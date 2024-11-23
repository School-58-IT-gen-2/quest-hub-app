from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class AbstractModel(ABC):
    """Абстрактный класс сущности"""

    @abstractmethod
    def __dict__(self):
        pass

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def get_by_id(self):
        pass

    @abstractmethod
    def get_by_value(self):
        pass