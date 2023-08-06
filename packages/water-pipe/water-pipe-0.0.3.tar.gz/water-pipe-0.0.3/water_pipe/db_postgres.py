from itertools import chain
import psycopg2
import re

from water_pipe.base import Connect, DTYPE

class PostgresConnect(Connect):
    
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
        config["user"] = config.pop("username")
        
        self.connect = psycopg2.connect(**config)
        self.cursor = self.connect.cursor()
        
        self.std_schema_data = []
        self.dataset_comment = ""
        self.placeholders = ""
        
        self.dtype_map = {
            "tinyint": ["int2"],
            "int": ["int4"],
            "bigint": ["int8"],
            "float": ["float"],
            "double": ["float"],
            "decimal": ["numeric"],
            "char": ["char"],
            "varchar": ["varchar"],
            "text": ["text"],
            "date": ["date"],
            "time": ["time"],
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
        one_data = list(chain.from_iterable(data))  # 二维列表转一维列表
        # print(one_data)
        n_placeholders = ",".join([f"({self.placeholders})"] * len(data))
        # print(n_placeholders)
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
               t1.udt_name as col_type, 
               coalesce(t1.character_maximum_length, t1.numeric_precision) as precision,  
               t1.numeric_scale as scale,
               -- case when t1.udt_name like '%int%' then 'int'
               --      when t1.udt_name like '%float%' then 'float'
               -- 	   when t1.udt_name like '%numeric%' then concat('numeric(', t1.numeric_precision, ',' , t1.numeric_scale, ')')
               --      when t1.udt_name like '%varchar%' then concat(t1.udt_name, case when t1.character_maximum_length is null then '' else '(' ||t1.character_maximum_length || ')' end)
               -- 	   when t1.udt_name like '%char%' then concat('char', case when t1.character_maximum_length is null then '' else '(' ||t1.character_maximum_length || ')' end)
               --      else t1.udt_name end as data_type,
               t3.description as comment,
               t4.description as dataset_comment
	    from information_schema.columns as t1
	    join pg_catalog.pg_class as t2 on t1.table_name = t2.relname
	    left join pg_catalog.pg_description as t3 on t2.oid = t3.objoid and t1.ordinal_position = t3.objsubid
	    left join pg_catalog.pg_description as t4 on t2.oid = t4.objoid and t4.objsubid = 0
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
        # print(dtype)
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
