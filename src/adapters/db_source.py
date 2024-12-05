from typing import List
from pydantic import SecretStr
from supabase.client import ClientOptions
from supabase import create_client, Client
from adapters.abstract_source import AbstractSource


class DBSource(AbstractSource):
    """Адаптер для работы с базой данных"""

    def __init__(self, url: str, key: SecretStr):
        """
        :param str url: Ссылка на supabase
        :param str key: Ключ от supabase
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

        :param str table_name: Название таблицы
        :return List[dict]: Список из словаря
        """
        return dict(self.__supabase.table(table_name).select().execute())["data"]

    def get_by_id(self, table_name: str, id: str | int) -> List[dict]:
        """
        Получение объекта по id

        :param str table_name: Название таблицы
        :param int id: id объекта
        :return List[dict]: Список из словаря со строкой таблицы
        """
        return dict(self.__supabase.table(table_name).select().eq("id", id).execute())[
            "data"
        ]

    def get_by_value(
        self,
        table_name: str,
        parameter: str,
        parameter_value: any,
    ) -> List[dict]:
        """
        Получение объекта по значению определенного параметра

        :param str table_name: Название таблицы
        :param str parameter: Столбец, по которому происходит сравнение
        :param str / int / list parameter_value: Значение, по которому происходит сравнение
        :return List[dict]: Список из словаря со строкой таблицы
        """
        return dict(
            self.__supabase.table(table_name)
            .select()
            .eq(parameter, parameter_value)
            .execute()
        )["data"]

    def insert(self, table_name: str, insert_dict: dict) -> List[dict]:
        """
        Вставка строки в таблицу

        :param str table_name: Название таблицы
        :param dict dict: Словарь с данными для новой строки
        :return List[dict]: Список из словаря с новой строкой
        """
        return dict(self.__supabase.table(table_name).insert(insert_dict).execute())[
            "data"
        ]

    def update(self, table_name: str, update_dict: dict, id: int) -> List[dict]:
        """
        Изменение строки в таблице

        :param str table_name: Название таблицы
        :param dict dict: Словарь с данными для новой строки
        :param int id: id строки, которую нужно изменить
        :return List[dict]: Список из словаря с новой строкой
        """
        return dict(
            self.__supabase.table(table_name).update(update_dict).eq("id", id).execute()
        )["data"]

    def delete(self, table_name: str, id: int) -> List[dict]:
        """
        Удаление строки из таблицы

        :param str table_name: Название таблицы
        :param int id: id строки, которую нужно удалить
        :return List[dict]: Список из словаря с удалённой строкой
        """
        return dict(self.__supabase.table(table_name).delete().eq("id", id).execute())[
            "data"
        ]
