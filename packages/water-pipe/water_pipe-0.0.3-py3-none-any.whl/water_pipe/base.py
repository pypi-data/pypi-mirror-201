from abc import ABC, abstractmethod


class Connect(ABC):

    @abstractmethod
    def execute(self, sql):
        pass

    @abstractmethod
    def query(self, sql):
        pass

    @abstractmethod
    def table(self, table_name):
        pass

    @abstractmethod
    def insert(self, table_name):
        pass


class DTYPE:

    def __init__(self, name: str, precision: int = None, scale: int = None):
        self.name = name
        self.precision = precision
        self.scale = scale

    def get(self) -> str:
        if self.precision and self.scale:
            return f"{self.name}({self.precision},{self.scale})"

        if self.precision:
            return f"{self.name}({self.precision})"

        return self.name

    def __str__(self) -> str:
        return f"name={self.name}, precision={self.precision}, scale={self.scale}"
