from pyhive import hive

from water_pipe.base import Connect

class HiveConnect(Connect):
    
    def __init__(self, config) -> None:
        """
        config = {
            
        }
        """
        
        self.connect = hive.connect(config)