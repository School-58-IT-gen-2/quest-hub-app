from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List


class AbstractSource(ABC):
    @abstractmethod
    def get_all(self, collection_name: str) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id(self, collection_name: str, object_id: int) -> dict:
        pass

    @abstractmethod
    def insert(self, collection_name: str, document: dict) -> dict:
        pass

    @abstractmethod
    def update(self, collection_name: str, object_id: int, document: dict) -> dict:
        pass

    @abstractmethod
    def delete(self, collection_name: str, object_id: int) -> dict:
        pass