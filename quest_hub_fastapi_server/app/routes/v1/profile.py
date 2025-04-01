from fastapi import APIRouter, HTTPException

from quest_hub_fastapi_server.modules.profile import Profile
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.profile.models import (
    ProfileRequest,
    ProfilePutRequest,
)

from logs.log import function_log

profile_route = APIRouter(prefix="/profiles", tags=["profiles"])

# @function_log
@profile_route.post(path="/user")
def create_user(
    body: ProfileRequest
):
    """
        Создание пользователя.
        Args:
            body (ProfileRequest): Данные пользователя.
        Returns:
            response (dict): Данные пользователя.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    new_user = Profile(
        body.tg_id,
        new_db_source,
        body.first_name,
        body.username,
        body.last_name,
        body.role,
        age=body.age,
        is_bot=body.is_bot,
        language_code=body.language_code,
        is_premium=body.is_premium,
    )
    user = new_user.insert()
    return user

# @function_log
@profile_route.get(path="/profile")
def get_user(tg_id: int):
    """
        Получение данных пользователя.

        Args:
            tg_id (int): ID пользователя.
        Returns:
            response (dict): Данные пользователя.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    new_user = Profile(tg_id, new_db_source)
    new_user.insert()
    return new_user.__dict__()

# @function_log
@profile_route.delete(path="/user")
def delete_user(tg_id: int):
    """
        Удаление пользователя.

        Args:
            tg_id (int): ID пользователя.
        Returns:
            response (dict): Данные пользователя.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key) 
    new_db_source.connect()       
    new_user = Profile(tg_id, new_db_source)
    new_user.insert()
    return new_user.delete()

# @function_log
@profile_route.put(path="/user")
def edit_user(
    body: ProfilePutRequest
    ):
    """
        Редактирование данных пользователя.
        Args:
            body (ProfilePutRequest): Данные пользователя.
        Returns:
            response (dict): Данные пользователя.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    new_user = Profile(body.tg_id, new_db_source)
    new_user.insert()
    return new_user.update({
                "first_name": body.first_name,
                "username": body.username,
                "age": body.age,
                "last_name": body.last_name,
                "is_premium": body.is_premium,
                "language_code": body.language_code
                })
