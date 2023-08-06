from itertools import chain
import MySQLdb

from water_pipe.base import Connect, DTYPE

class MysqlConnect(Connect):
        
    def __init__(self, norm_config) -> None:
        """
        norm_config = {
            "host": "127.0.0.1",
            "username": "admin",
            "password": "admin123",
            "database": "test",
            "port": 3306,
            ......
        }
        """
        config = norm_config.copy()
        config["user"] = norm_config.pop("username")
        
        self.connect = MySQLdb.connect(**config)
        self.cursor = self.connect.cursor()
        
        self.std_schema_data = []
        self.dataset_comment = ""
        self.placeholders = ""
        
        self.dtype_map = {
            "tinyint": ["tinyint", "smallint"],
            "int": ["int", "mediumint"],
            "bigint": ["bigint"],
            "float": ["float"],
            "double": ["double"],
            "decimal": ["decimal"],
            "char": ["char"],
            "varchar": ["varchar"],
            "text": ["text"],
            "date": ["date"],
            "time": ["time"],
            "datetime": ["datetime"],
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
        one_data = list(chain.from_iterable(data))  # 二维列表转一维列表
        print(one_data)
        n_placeholders = ",".join([f"({self.placeholders})"] * len(data))
        print(n_placeholders)
        self.cursor.execute("insert into {} values {}".format(table_name, n_placeholders), one_data)
        # self.cursor.executemany("insert into {} values ({})".format(table_name, self.placeholders), data)
    
    def set_query_schema(self, sql):
        type_sql = "select oid, typname from pg_type where oid < 10000"
        self.cursor.execute(type_sql)
        type_map = {}
        for row in self.cursor.fetchall():
            type_map[row[0]] = row[1]
        
        self.cursor.execute("select * from (" + sql + ") t limit 0")
        for row in self.cursor.description:
            col_name = row[0]
            data_type = self.convert_std_dtype(DTYPE(type_map[row[1]], row[4], row[5]))
            comment = ""
            self.std_schema_data.append([col_name, data_type, comment])
        self.placeholders = ",".join(["%s"] * len(self.std_schema_data))
    
    def set_table_schema(self, table_name):
        # sql result: [col_name, col_type, precision, scale, column_comment, table_comment]
        sql = f"""
        select t1.column_name as col_name,
               t1.data_type as col_type, 
               coalesce(t1.character_maximum_length, t1.numeric_precision) as `precision`,  
               t1.numeric_scale as scale,
               t1.column_comment,
               t2.table_comment
	    from information_schema.columns as t1
	    join information_schema.tables t2 on t1.table_schema=t2.table_schema and t1.table_name=t2.table_name
	    where concat(t1.table_schema, '.', t1.table_name) = '{table_name}'
	    order by t1.ordinal_position
        """
        self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            col_name = row[0]
            data_type = self.convert_std_dtype(DTYPE(row[1], row[2], row[3]))
            comment = row[4]
            self.std_schema_data.append([col_name, data_type, comment])
            self.dataset_comment = row[5]
        self.placeholders = ",".join(["%s"] * len(self.std_schema_data))
    
    def convert_std_dtype(self, dtype) -> DTYPE:
        print(dtype)
        if dtype.get() in ["varchar", "unknown"]:
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
        cols_comment_list = []
        for row in self.std_schema_data:
            col_name = row[0]
            # dtype = self.convert_self_dtype(row[1])
            data_type = self.convert_self_dtype(row[1]).get()
            comment = row[2]
            cols_list.append("    {:<30} {}".format(col_name, data_type))
            if comment:
                cols_comment_list.append(f"\ncomment on column {table_name}.{col_name} is '{comment}';")
        
        sql = f"create table if not exists {table_name} (\n" + \
            ",\n".join(cols_list) + \
            "\n);"
        if self.dataset_comment:
            sql += f"\ncomment on table {table_name} is '{self.dataset_comment}';"
        if cols_comment_list:
            sql += "".join(cols_comment_list)
        print(sql)
        self.cursor.execute(sql)