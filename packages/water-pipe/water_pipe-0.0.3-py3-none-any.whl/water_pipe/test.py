
from channel import DataChannel

if __name__=='__main__':
    impala_db_config = {
        "driver": "impala",
        "config": {
            "host": "10.63.82.218",
            "username": "work",
            "password": "TwkdFNAdS1nIikzk",
            "database": "default",
            "port": 21050,
            "auth_mechanism": "LDAP",
        }
    }
    pg_db_config = {
        "driver": "postgres",
        "config": {
            "host": "10.63.82.191",
            "username": "dw_rw",
            "password": "Yxsj@123",
            "database": "test",
            "port": 5432
        }
    }
    csv_db_config = {
        "driver": "csv",
        "config": {
            "filename": "data",
            # "path": ""
        }
    }
    # with DataChannel(impala_db_config, pg_db_config) as channel:
    #     channel.table("tmp.t2")
    #     # channel.sink_db.execute("truncate table medical.t2")
    #     channel.insert("medical.t2", 2, is_create=True)
    
    # with DataChannel(pg_db_config, impala_db_config) as channel:
    #     channel.query("select * from medical.t2 limit 9")
    #     channel.insert("tmp.t3", 2, is_create=True)
    
    # with DataChannel(pg_db_config, csv_db_config) as channel: 
    #     channel.query("select * from medical.dim_date limit 123")
    #     channel.insert(is_create=True)
        
    with DataChannel(csv_db_config, pg_db_config) as channel: 
        channel.query()
        channel.insert("medical.t_csv", 2, is_create=True)
        
        