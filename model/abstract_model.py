from abc import ABC, abstractmethod


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

    @abstractmethod
    def synchronize(self):
        pass

    @abstractmethod
    def set_attributes(self):
        pass