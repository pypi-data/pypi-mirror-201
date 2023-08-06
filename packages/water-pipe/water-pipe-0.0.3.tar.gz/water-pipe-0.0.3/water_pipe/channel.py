from datetime import datetime
from loguru import logger


class DataChannel:

    def __init__(self, source_config, sink_config):
        # driver_map = {
        #     # "mysql": MySQLdb.connect(**sink_config.config),
        #     "oracle": "cx_Oracle.connect()",
        #     # "mssql": pymssql.connect(**source_config.config),
        #     # "postgres": psycopg2.connect(**source_config["config"]),
        #     "postgres": PostgresConnect,
        #     # "hive": hive.connect(**source_config["config"]),
        #     "impala": ImpalaConnect,
        # }

        # 动态导入, 主要是避免安装所有数据库的依赖包, 用什么数据库安装什么数据库即可
        self.source_driver = source_config["driver"]
        self.sink_driver = sink_config["driver"]
        source_module = __import__(f"water_pipe.db_{self.source_driver}", fromlist=[f"db_{self.source_driver}"])
        sink_module = __import__(f"water_pipe.db_{self.sink_driver}", fromlist=[f"db_{self.sink_driver}"])
        source_class = getattr(source_module, self.source_driver.capitalize() + "Connect")
        sink_class = getattr(sink_module, self.sink_driver.capitalize() + "Connect")

        self.source_db = source_class(source_config["config"])
        self.sink_db = sink_class(sink_config["config"])
        self.dataset = []
        self.start_time = datetime.now()
        # print(self.start_time)  # __init__ 比 __enter__ 优先执行

    def source_execute(self, sql):
        logger.info("source db execute: " + sql)
        self.source_db.execute(sql)

    def sink_execute(self, sql):
        logger.info("sink db execute: " + sql)
        self.sink_db.execute(sql)

    def query(self, sql=None):
        self.dataset = self.source_db.query(sql)
        self.sink_db.std_schema_data = self.source_db.std_schema_data
        self.sink_db.dataset_comment = self.source_db.dataset_comment
        self.sink_db.placeholders = self.source_db.placeholders

    def table(self, table_name):
        self.dataset = self.source_db.table(table_name)
        self.sink_db.std_schema_data = self.source_db.std_schema_data
        self.sink_db.dataset_comment = self.source_db.dataset_comment
        self.sink_db.placeholders = self.source_db.placeholders

    def insert(self, sink_table=None, batch_size=1000, is_create=False, header=True):

        if is_create:
            if self.sink_driver in ["csv", "excel"]:
                self.sink_db.create_table(header=header)
            else:
                self.sink_db.create_table(sink_table)

        i = 0
        start_time = datetime.now()
        logger.info("starting insert ......")
        while True:
            data = self.dataset(batch_size)
            if data:
                n = len(data)
                j = i + n

                if self.sink_driver in ["csv", "excel"]:
                    self.sink_db.insert(data)
                else:
                    self.sink_db.insert(sink_table, data)

                elapsed_time = datetime.now() - start_time
                duration = 1 if elapsed_time.seconds == 0 else elapsed_time.seconds
                speed = int(j / duration)
                # progress = "{:.2f}".format(j / row_count * 100)
                logger.info(f"insert into {sink_table} {j} data succeed, speed {speed} records/s, elapsed time {elapsed_time}")
                i += n
            else:
                break

    def __enter__(self):
        logger.debug("init at " + str(datetime.now()))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self.source_db, "cursor") and self.source_db.cursor:
            self.source_db.cursor.close()
            logger.debug(str(self.source_db.cursor) + " cursor closed")
        if hasattr(self.sink_db, "cursor") and self.sink_db.cursor:
            self.sink_db.cursor.close()
            logger.debug(str(self.sink_db.cursor) + " cursor closed")
        if hasattr(self.source_db, "connect") and self.source_db.connect:
            self.source_db.connect.commit()
            self.source_db.connect.close()
            logger.debug(str(self.source_db.connect) + " connect closed")
        if hasattr(self.sink_db, "connect") and self.sink_db.connect:
            self.sink_db.connect.commit()
            self.sink_db.connect.close()
            logger.debug(str(self.sink_db.connect) + " connect closed")
        logger.info(f"Total time: {datetime.now() - self.start_time}s")
