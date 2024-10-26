from __future__ import annotations
import time
import datetime
from adapters.abstract_source import AbstractSource
from typing import List, Optional, Tuple
import psycopg2
from psycopg2 import errorcodes


class DBSource(AbstractSource):
    """Адаптер для работы с базой данных"""

    def __init__(self, host, user, password, db_name='quest_hub_app'):
        """
            :param host: Хост
            :param user: Пользователь
            :param password: Пароль
            :param db_name: Название БД
        """
        self.__connection_data = {"host": host, 
                                  "user": user, 
                                  "password": password, 
                                  "dbname": db_name
                                  }
        self.__conn = None

    def connect(self, retry_count: int = 2) -> None:
        """
            Подключение к БД

            :param retry_count: Количество попыток повторного входа
        """
        if self.__conn:
            return
        for i in range(retry_count + 1):
            try:
                self.__conn = psycopg2.connect(**self.__connection_data)
                break
            except psycopg2.Error:
                time.sleep(5)

    def get_by_query(self, table_name: str, query: dict) -> List[dict]:
        """
        Возвращает запрошенный по query объект класса по данным из сохранений

        :param query: Пары ключ-значение для поиска
        :param db_source: data_source объект
        :return: Объект этого класса с таким id
        """
        self.connect()
        pairs = query.items()
        request = f'SELECT * FROM "{table_name}" WHERE '
        request += ' AND '.join([f'{i[0]}=\'{i[1]}\'' for i in pairs])
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request, list(query.values()))
        data = cursor.fetchall()
        desc = cursor.description

        return self.__format_Tuple_to_dict(data, desc)

    def run_query(self, query):
        """
        Выполнение запроса для БД

        :param query: Запрос
        """
        self.connect()
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, query)
        data = cursor.fetchall()
        self.__conn.commit()

        return data

    def get_all(self, collection_name: str) -> List[dict]:
        """
        Получение всех данных таблицы

        :param collection_name: Название таблицы
        :return: Список из словарей
        """
        self.connect()
        request = f'SELECT * FROM "{collection_name}"'
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request)
        data = cursor.fetchall()
        desc = cursor.description
        self.__conn.commit()
        return self.__format_Tuple_to_dict(data, desc)

    def get_by_id(self, collection_name: str, id: int) -> dict:
        """
        Получение объекта по id

        :param collection_name: Название таблицы
        :param id: id объекта
        :return: Словарь
        """
        self.connect()
        request = f'SELECT * FROM "{collection_name}" WHERE id={id}'
        cursor = self.__conn.cursor()
        self.__cursor_execute_wrapper(cursor, request)
        data = cursor.fetchall()
        desc = cursor.description
        if len(data) == 0:
            self.__conn.commit()
            raise ValueError(f'Объект с id {id} из {collection_name} не существует')
        return self.__format_Tuple_to_dict(data, desc)[0]

    def insert(self, collection_name: str, document: dict) -> dict:
        self.connect()
        cursor = self.__conn.cursor()
        try:
            cursor.execute(f'SELECT * FROM "{collection_name}" LIMIT 0')
        except psycopg2.Error as e:
            if errorcodes.lookup(e.pgcode) == 'UNDEFINED_TABLE':
                self.__conn.commit()
                raise ValueError('Данной таблицы не существует.')

        desc = [x[0] for x in cursor.description]
        values = [self.__wrap_string(document[x]) if x != 'id' else 'default' for x in desc]
        request = f'INSERT INTO "{collection_name}" VALUES ({",".join(map(str, values))}) RETURNING *;'
        try:
            cursor.execute(request)
        except psycopg2.Error as e:
            self.__conn.commit()
            if errorcodes.lookup(e.pgcode) == 'UNIQUE_VIOLATION':
                raise ValueError('ID добавляемого объекта уже существует.')
            elif errorcodes.lookup(e.pgcode) == 'FOREIGN_KEY_VIOLATION':
                raise ValueError('Один из ID связанных объектов недействителен.')
            elif errorcodes.lookup(e.pgcode) == 'INVALID_TEXT_REPRESENTATION':
                raise TypeError('Ошибка в типах данных.')
            raise ValueError(f"Неизвестная ошибка при добавлении новой записи в {collection_name}. "
                             f"Код ошибки: {errorcodes.lookup(e.pgcode)}")
        self.__conn.commit()
        new_obj = cursor.fetchone()
        new_doc = {desc[index]: new_obj[index] for index in range(len(desc))}
        return new_doc

    def update(self, collection_name: str, id: int | str | None, document: dict) -> dict:
        self.connect()
        cursor = self.__conn.cursor()
        document.pop('id')
        collection = collection_name
        req_data = []
        for elem in document:
            req_data.append(f"{elem} = {self.__wrap_string(document.get(elem))}")
        try:
            request = f'UPDATE "{collection}" SET {", ".join(req_data)} WHERE id = {str(id)}'
            cursor.execute(request)
            self.__conn.commit()
            return document
        finally:
            self.__conn.commit()

    def delete(self, collection_name: str, id: int | str | None):
        """
        Удаление из БД по id

        :param collection_name: Название таблицы
        :param id: id объекта
        """
        self.connect()
        cursor = self.__conn.cursor()

        collection = collection_name
        try:
            request = f'DELETE FROM "{collection}" WHERE id = {id}'
            cursor.execute(request)
        finally:
            self.__conn.commit()

    @staticmethod
    def __wrap_string(value: Optional[str]) -> str:
        if value is None:
            # Для базы None записывается по-другому
            return 'null'
        elif type(value) == str or type(value) == datetime.date:
            # Дата и строки должны быть в ковычках
            return f"'{value}'"
        else:
            return value

    @classmethod
    def __format_Tuple_to_dict(cls, data: list, desc: list) -> list[dict]:
        """
        Преобразование списка в список словарей

        :param data: Список значений
        :param desc: Список названий полей
        :return: Объект этого класса с таким id
        """
        to_return = []
        for i in data:
            to_return.append({desc[j].name: i[j] for j in range(len(desc))})
        return to_return

    @classmethod
    def __cursor_execute_wrapper(cls, cursor: any, request: str, params=None):
        try:
            cursor.execute(request, params)
        except psycopg2.Error as e:
            if errorcodes.lookup(e.pgcode) == 'UNDEFINED_TABLE':
                raise ValueError(f'Ошибка во время выполнения запроса, таблица не существует. Запрос: {request}')
            else:
                raise ValueError(f'Неизвестная ошибка во время выполнения запроса, '
                                 f'код ошибки: {errorcodes.lookup(e.pgcode)}. Запрос: {request}')