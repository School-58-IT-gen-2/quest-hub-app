from abc import ABC, abstractmethod
from typing import List
from logs.log import function_log


class AbstractSource(ABC):
    # @function_log
    @abstractmethod
    def get_all(self, table_name: str) -> List[dict]:
        pass

    # @function_log
    @abstractmethod
    def get_by_id(self, table_name: str, id: int) -> List[dict]:
        pass
    
    # @function_log
    @abstractmethod
    def insert(self, table_name: str, dict: dict) -> List[dict]:
        pass

    # @function_log
    @abstractmethod
    def update(self, table_name: str, dict: dict, id: int) -> List[dict]:
        pass

    # @function_log
    @abstractmethod
    def delete(self, table_name: str, id: int) -> List[dict]:
        pass

    # @function_log
    @abstractmethod
    def get_by_value(self, table_name: str, query: dict) -> List[dict]:
        pass
