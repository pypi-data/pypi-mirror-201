import csv
from pathlib import Path

from water_pipe.base import Connect, DTYPE

class CsvConnect(Connect):
    def __init__(self, norm_config) -> None:
        """
        norm_config = {
            "path": "/home/",
            "filename": "data",
            "separator": ",",
            "quoting": "",  # 
            ......
        }
        """
        config = norm_config.copy()
        
        # self.connect = None
        self.cursor = None
        
        self.std_schema_data = []
        self.dataset_comment = ""
        self.placeholders = ""
        
        path = config.get("path") if config.get("path") else "."
        filename = config["filename"]
        separator = config.get("separator") if config.get("separator") else ","
        quote = csv.QUOTE_MINIMAL
        
        self.file = Path(path).joinpath(filename + ".csv")
        self.data = None
        
        # register
        csv.register_dialect("dialect", delimiter=separator, quoting=quote)
        
    def execute(self, sql):
        raise Exception("Not Supported")
        
    def query(self, sql):
        self.set_query_schema()
        self.cursor = open(self.file, "r", encoding="utf-8", newline="")
        reader = csv.reader(self.cursor, "dialect")
        reader.__next__()  # 跳过header
        self.data = iter(row for row in reader)
        return self.fetchmany
    
    def set_query_schema(self):
        """ return dataset schema: col_name, data_type, comment"""
        with open(self.file, "r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for col_name in reader.fieldnames:
                self.std_schema_data.append([col_name, DTYPE("text"), ""])
        self.placeholders = ",".join(["%s"] * len(self.std_schema_data))
    
    def fetchmany(self, size):
        batch_data = []
        for _ in range(size):
            try:
                batch_data.append(next(self.data))
            except StopIteration:
                break
        return batch_data

    def table(self, table_name):
        raise Exception("Not Supported")
    
    def insert(self, data):
        with open(self.file, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, "dialect")
            writer.writerows(data)
    
    def create_table(self, header=True):
        with open(self.file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, "dialect")
            if header:
                header_data = [x[0] for x in self.std_schema_data]
                writer.writerow(header_data)
