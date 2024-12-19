from abc import ABC, abstractmethod
from typing import List


class AbstractModel(ABC):
    """Абстрактный класс сущности"""

    @abstractmethod
    def __dict__(self) -> dict:
        pass

    @abstractmethod
    def insert(self) -> dict:
        pass

    @abstractmethod
    def update(self) -> List[dict]:
        pass

    @abstractmethod
    def delete(self) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id(self) -> List[dict]:
        pass

    @abstractmethod
    def get_by_value(self) -> List[dict]:
        pass

    @abstractmethod
    def synchronize(self) -> None:
        pass

    @abstractmethod
    def set_attributes(self) -> None:
        pass
