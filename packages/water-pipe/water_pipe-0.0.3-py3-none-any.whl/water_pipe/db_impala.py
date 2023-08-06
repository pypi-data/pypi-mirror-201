from impala import dbapi
from itertools import chain
import re

from water_pipe.base import Connect, DTYPE

class ImpalaConnect(Connect):

    def __init__(self, norm_config) -> None:
        """
        norm_config = {
            "host": "127.0.0.1",
            "username": "admin",
            "password": "admin123",
            "database": "test",
            "port": 5432,
            ......
        }
        """
        config = norm_config.copy()
        config["user"] = norm_config.pop("username")

        self.connect = dbapi.connect(**config)
        self.cursor = self.connect.cursor()

        self.std_schema_data = []
        self.dataset_comment = ""
        self.placeholders = ""

        self.dtype_map = {
            # 必须都要对应
            "tinyint": ["tinyint"],
            "int": ["int"],
            "bigint": ["bigint"],
            "float": ["float"],
            "double": ["double"],
            "decimal": ["decimal"],
            "char": ["char"],
            "varchar": ["varchar"],
            "text": ["string"],
            "date": ["timestamp"],
            "time": ["timestamp"],
            "datetime": ["timestamp"],
            "timestamp": ["timestamp"],
        }

    def execute(self, sql):
        self.cursor.execute(sql)

    def query(self, sql):
        self.set_query_schema(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchmany

    def table(self, table_name):
        self.set_table_schema(table_name)
        self.cursor.execute(f"select * from {table_name}")
        return self.cursor.fetchmany

    def insert(self, table_name, data):
        # TODO
        # print(data)

        # 一批数据会产生一个文件 OPTIMIZE
        # one_data = list(chain.from_iterable(data))  # 二维列表转一维列表
        # n_placeholders = ",".join([f"({self.placeholders})"] * len(data))
        # self.cursor.execute("insert into {} values {}".format(table_name, n_placeholders), one_data)

        # 一条数据会产生一个文件 OPTIMIZE
        self.cursor.executemany("insert into {} values ({})".format(table_name, self.placeholders), data)

    def set_query_schema(self, sql):
        """ return dataset schema: col_name, data_type, comment"""
        self.cursor.execute("select * from (" + sql + ") t limit 0")
        for row in self.cursor.description:
            col_name = row[0]
            data_type = self.convert_std_dtype(DTYPE(str(row[1]).lower(), row[4], row[5]))
            comment = row[2]
            self.std_schema_data.append([col_name, data_type, comment])
        self.placeholders = ",".join(["%s"] * len(self.std_schema_data))

    def set_table_schema(self, table_name):
        """ return dataset schema: col_name, data_type, comment """
        
        def split_str_type(str_type : str) -> DTYPE:
            result = re.search(r"(.*)\((.*),(.*)\)", str_type)
            if result:
                col_type = result.group(1)
                precision = result.group(2)
                scale = result.group(3)
                return DTYPE(col_type, precision, scale)
            
            result = re.search(r"(.*)\((.*)\)", str_type)
            if result:
                col_type = result.group(1)
                precision = result.group(2)
                return DTYPE(col_type, precision)
            
            return DTYPE(str_type)
        
        sql = f"describe {table_name}"
        self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            col_name = row[0]
            data_type = self.convert_std_dtype(split_str_type(row[1]))
            comment = row[2]
            self.std_schema_data.append([col_name, data_type, comment])
            # self.dataset_comment = row[3]  #  describe无法获取表备注 TODO
        self.placeholders = ",".join(["%s"] * len(self.std_schema_data))

    def convert_std_dtype(self, dtype) -> DTYPE:
        # print(dtype)
        if dtype.get() == "varchar":
            return DTYPE("string")
        if dtype.get() == "numeric":
            return DTYPE("decimal", 38, 4)
        
        for key in self.dtype_map:
            types = self.dtype_map[key]
            for type in types:
                if type == dtype.name:
                    dtype.name = key
                    return dtype
        print(f"ERROR: self to std: {dtype} ==> varchar(128)")
    
    def convert_self_dtype(self, dtype) -> DTYPE:
        for key in self.dtype_map:
            if key == dtype.name:
                dtype.name = self.dtype_map[key][0]
                return dtype
        print(f"ERROR: std to self: {dtype} ==> varchar(128)")

    def create_table(self, table_name):
        cols_list = []
        for row in self.std_schema_data:
            col_name = row[0]
            data_type = self.convert_self_dtype(row[1]).get()
            comment = f"comment '{row[2]}'" if row[2] else ""
            cols_list.append("    {:<30} {:<10} {}".format(
                col_name, data_type, comment))

        sql = f"create table if not exists {table_name} (\n" + \
            ",\n".join(cols_list) + \
            "\n);"
        if self.dataset_comment:
            sql += f"\ncomment '{self.dataset_comment}';"
        print(sql)
        self.cursor.execute(sql)
