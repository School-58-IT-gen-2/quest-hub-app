from adapters.abstract_source import AbstractSource
from typing import List
from supabase import create_client, Client
from supabase.client import ClientOptions


class DBSource(AbstractSource):
    """Адаптер для работы с базой данных"""

    def __init__(self, url: str, key: str):
        """
            :param url: Ссылка на supabase
            :param key: Ключ от supabase
        """
        self.__url = url
        self.__key = key.get_secret_value()

    def connect(self) -> None:
        """Подключение к БД"""
        try:
            supabase: Client = create_client(
                supabase_url=self.__url,
                supabase_key=self.__key,
                options=ClientOptions(
                    postgrest_client_timeout=10,
                    storage_client_timeout=10,
                    schema="public",
                ),
            )
            self.__supabase = supabase
        except Exception as error:
            print(f"Error: {error}")

    def get_all(self, table_name: str) -> List[dict]:
        """
        Получение всех данных таблицы

        :param table: Название таблицы
        :return: Список из словаря
        """
        return self.__supabase.table(table_name).select().execute()

    def get_by_id(self, table_name: str, id: int) -> List[dict]:
        """
        Получение объекта по id

        :param table_name: Название таблицы
        :param id: id объекта
        :return: Список из словаря со строкой таблицы
        """
        return self.__supabase.table(table_name).select().eq("id", id).execute()

    def insert(self, table_name: str, dict: dict) -> List[dict]:
        """
        Вставка строки в таблицу

        :param table_name: Название таблицы
        :param dict: Словарь с данными для новой строки
        :return: Список из словаря с новой строкой
        """
        return self.__supabase.table(table_name).insert(dict).execute()

    def update(self, table_name: str, dict: dict, id: int) -> List[dict]:
        """
        Изменение строки в таблице

        :param table_name: Название таблицы
        :param dict: Словарь с данными для новой строки
        :param id: id строки, которую нужно изменить
        :return: Список из словаря с новой строкой
        """
        return self.__supabase.table(table_name).update(dict).eq("id", id).execute()

    def delete(self, table_name: str, id: int) -> List[dict]:
        """
        Удаление строки из таблицы

        :param table_name: Название таблицы
        :param id: id строки, которую нужно удалить
        :return: Список из словаря с удалённой строкой
        """
        return self.__supabase.table(table_name).delete().eq("id", id).execute()
