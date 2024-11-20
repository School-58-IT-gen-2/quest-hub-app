from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List


class AbstractSource(ABC):
    @abstractmethod
    def get_all(self, table_name: str) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id(self, table_name: str, id: int) -> List[dict]:
        pass

    @abstractmethod
    def insert(self, table_name: str, dict: dict) -> List[dict]:
        pass

    @abstractmethod
    def update(self, table_name: str, dict: dict, id: int) -> List[dict]:
        pass

    @abstractmethod
    def delete(self, table_name: str, id: int) -> List[dict]:
        pass

    """@abstractmethod
    def get_by_query(self, table_name: str, query: dict) -> List[dict]:
        pass"""