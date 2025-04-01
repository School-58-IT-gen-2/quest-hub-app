from abc import ABC, abstractmethod
from typing import List

from logs.log import function_log

class AbstractModel(ABC):
    """Абстрактный класс сущности"""

    # @function_log
    @abstractmethod
    def __dict__(self) -> dict:
        pass

    # @function_log
    @abstractmethod
    def insert(self) -> dict:
        pass

    # @function_log
    @abstractmethod
    def update(self) -> List[dict]:
        pass

    # @function_log
    @abstractmethod
    def delete(self) -> List[dict]:
        pass

    # @function_log
    @abstractmethod
    def get_by_id(self) -> List[dict]:
        pass

    # @function_log
    @abstractmethod
    def get_by_value(self) -> List[dict]:
        pass

    # @function_log
    @abstractmethod
    def synchronize(self) -> None:
        pass

    # @function_log
    @abstractmethod
    def set_attributes(self) -> None:
        pass
