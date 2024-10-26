from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class AbstractModel(ABC):
    """Абстрактный класс сущности"""

    def __init__(self, db_source: DBSource):
        self._db_source = db_source

    @classmethod
    def _get_collection_name(cls) -> str:
        return cls.__name__

    def save(self) -> AbstractModel:
        if self.get_main_id() is None:
            result = self._db_source.insert(self._get_collection_name(), self.__dict__())
            self._set_main_id(result['id'])
        else:
            self._db_source.update(self._get_collection_name(), self.get_main_id(), self.__dict__())
        return self

    def delete(self) -> AbstractModel:
        if self.get_main_id() is not None:
            self._db_source.delete(self._get_collection_name(), self.get_main_id())
            self._set_main_id(None)
        return self

    def serialize_to_json(self, indent: Optional[int] = None) -> json:
        """
        Превращает данный объект класса в json-строку

        :param indent: Табуляция для полученной строки json
        :return: json-строка
        """
        return json.dumps(self.__dict__(), ensure_ascii=False, indent=indent)

    @classmethod
    def get_all(cls, db_source: DBSource) -> List[AbstractModel]:
        """
        Возвращает все данные из сохранений в формате объектов соответствующих классов

        :param db_source: data_source объект
        :return: Список всех объектов этого класса
        """
        return [cls(**obj, db_source=db_source) for obj in db_source.get_all(cls._get_collection_name())]

    @classmethod
    def get_by_id(cls, element_id: int, db_source: DBSource) -> AbstractModel:
        """
        Возвращает запрошенный по element_id объект класса по данным из сохранений

        :param element_id: id объекта
        :param db_source: data_source объект
        :return: Объект этого класса с таким идшником
        """

        obj = db_source.get_by_id(cls._get_collection_name(), element_id)
        return cls(**obj, db_source=db_source)

    @classmethod
    def get_by_query(cls, query: dict, db_source: DBSource) -> List[AbstractModel]:
        """
        Возвращает запрошенный по query объект класса по данным из сохранений

        :param query: Пары ключ-значение для поиска
        :param db_source: data_source объект
        :return: Объект этого класса с таким id
        """
        obj = db_source.get_by_query(cls._get_collection_name(), query)
        return [cls(**el, db_source=db_source) for el in obj]

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __dict__(self):
        pass

    def get_db_source(self) -> DBSource:
        return self._db_source

    def get_main_id(self) -> int:
        """
        Возвращает id текущего объекта

        :return: id текущего объекта
        """
        return self._id

    def _set_main_id(self, elem_id: Optional[int] = None) -> AbstractModel:
        """
        Меняет id текущего объекта на значение параметра

        :param elem_id: Новый id
        :return: Текущий объект
        """
        self._id = elem_id
        return self