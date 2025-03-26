from typing import List
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import SecretStr
from supabase.client import ClientOptions
from supabase import create_client, Client
import uuid

from quest_hub_fastapi_server.adapters.abstract_source import AbstractSource


class DBSource(AbstractSource):
    """Адаптер для работы с базой данных."""

    def __init__(self, url: str, key: SecretStr) -> None:
        """
        Args:
            url (str): Ссылка на supabase.
            key (str): Ключ от supabase.
        """
        self.__url = url
        self.__key = key.get_secret_value()

    def connect(self) -> None:
        """Подключение к базе данных."""
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
            response = supabase.table('profiles').select('*').execute()
            response.raise_when_api_error(response)
        except Exception as error:
            print(f"Error: {error}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Не удалось подключиться к базе данных",
            )

    def get_all(self, table_name: str) -> List[dict]:
        """
        Получение всех данных таблицы.

        Args:
            table_name (str): Название таблицы.

        Returns:
            List[dict]: Список из словаря.
        """
        return dict(self.__supabase.table(table_name).select().execute())["data"]

    def get_by_id(self, table_name: str, id: str | uuid.UUID) -> List[dict]:
        """
        Получение объекта по id.

        Args:
            table_name (str): Название таблицы.
            id (int): id объекта.
        
        Returns:
            List[dict]: Список из словаря со строкой таблицы.
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
        Получение объекта по значению определенного параметра.

        Args:
            table_name (str): Название таблицы.
            parameter (str): Столбец, по которому происходит сравнение.
            parameter_value (str / int / list): Значение, по которому происходит сравнение.

        Returns:
            List[dict]: Список из словаря со строкой таблицы.
        """
        return dict(
            self.__supabase.table(table_name)
            .select()
            .eq(parameter, parameter_value)
            .execute()
        )["data"]

    def insert(self, table_name: str, insert_dict: dict) -> List[dict]:
        """
        Вставка строки в таблицу.

        Args:
            table_name (str): Название таблицы.
            dict (dict): Словарь с данными для новой строки.
        
        Returns:
            List[dict]: Список из словаря с новой строкой.
        """
        return dict(self.__supabase.table(table_name).insert(insert_dict).execute())[
            "data"
        ]

    def update(self, table_name: str, update_dict: dict, id: str| uuid.UUID) -> List[dict]:
        """
        Изменение строки в таблице.

        Args:
            table_name (str): Название таблицы.
            dict (dict): Словарь с данными для новой строки.
            id (int): id строки, которую нужно изменить.

        Returns:
            List[dict]: Список из словаря с новой строкой.
        """
        return dict(
            self.__supabase.table(table_name).update(update_dict).eq("id", id).execute()
        )["data"]

    def delete(self, table_name: str, id: uuid.UUID) -> List[dict]:
        """
        Удаление строки из таблицы.

        Args:
            table_name (str): Название таблицы.
            id (int): id строки, которую нужно удалить.

        Returns:    
            List[dict]: Список из словаря с удалённой строкой.
        """
        return dict(self.__supabase.table(table_name).delete().eq("id", id).execute())[
            "data"
        ]