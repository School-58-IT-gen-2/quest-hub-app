import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
    Note,Item,
    BadRequestException,
    InternalServerErrorException,
    ServiceUnavailableException
)
from logs.log import function_log

char_route = APIRouter(prefix="/characters", tags=["characters"])

@function_log
@char_route.post(path="/char-list", response_model=CharListRequestModel)
async def add_character(character: CharListRequestModel):
    """
        Создание персонажа.

        Args:
            character (CharListRequestModel): Данные персонажа.
        Returns:
            response (dict): Данные персонажа.
        Raises:
            BadRequestException: Некорректный запрос.
            InternalServerErrorException: Внутренняя ошибка сервера.
            ServiceUnavailableException: Сервис временно недоступен.
    """
    #try:
    if not character:
        raise BadRequestException()
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    new_character = character.model_dump(exclude_unset=True)
    result = new_db_source.insert("character_list", new_character)
    if result:
        return result[0]
    else:
        raise ServiceUnavailableException()
    #except BadRequestException as e:
    #    raise e
    #except Exception as error:
    #    raise InternalServerErrorException()


@function_log
@char_route.put(path="/char-list", response_model=CharListRequestModel)
async def update_character(character_id: uuid.UUID|str, character: CharListRequestModel):
    """
        Обновление данных персонажа.

        Args:
            character_id (int): ID персонажа.
            character (CharListRequestModel): Данные персонажа.
        Returns:
            response (dict): Данные персонажа.
        Raises:
            BadRequestException: Некорректный запрос.
            InternalServerErrorException: Внутренняя ошибка сервера.
            NotFoundException: Персонаж не найден.
    """
    try:
        if not character_id or not character:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        updated_character = character.model_dump(exclude_unset=True)
        result = new_db_source.update("character_list", updated_character, character_id)
        if result:
            return result[0]
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except BadRequestException as e:
        raise e
    except Exception as error:
        raise InternalServerErrorException()


@function_log
@char_route.get(path="/char-list/{character_id}")
async def get_character(character_id: uuid.UUID|str):
    """
        Получение данных персонажа по ID.
        Args:
            character_id (int): ID персонажа.
        Returns:
            response (dict): Данные персонажа.
        Raises:
            BadRequestException: Некорректный запрос.
            NotFoundException: Персонаж не найден.
            InternalServerErrorException: Внутренняя ошибка сервера.
    """
    try:
        if not character_id:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character:
            return character
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except BadRequestException as e:
        raise e
    except Exception as error:
        raise InternalServerErrorException()


@function_log
@char_route.delete(path="/char-list/{character_id}")
async def delete_character(character_id: uuid.UUID|str):
    """
        Удаление персонажа по ID.
        Args:
            character_id (int): ID персонажа.
        Returns:
            response (dict): Данные персонажа.
        Raises:
            BadRequestException: Некорректный запрос.
            NotFoundException: Персонаж не найден.
            InternalServerErrorException: Внутренняя ошибка сервера.
    """
    try:
        if not character_id:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character:
            new_db_source.delete("character_list", character_id)
            return {"detail": "Character deleted successfully", "character": character}
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except BadRequestException as e:
        raise e
    except Exception as error:
        raise InternalServerErrorException()


@function_log
@char_route.get(path="/char-list/{user_id}/")
async def get_characters_by_user(user_id: str):
    """
        Получение персонажей по ID пользователя.
        Args:
            user_id (str): ID пользователя.
        Returns:
            response (list): Список персонажей.
        Raises:
            BadRequestException: Некорректный запрос.
            NotFoundException: Персонажи не найдены.
            InternalServerErrorException: Внутренняя ошибка сервера.
    """
    try:
        if not user_id:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        characters = new_db_source.get_by_value("character_list", "user_id", user_id)
        #if characters:
        return characters
        #else:
        #    raise HTTPException(
        #        status_code=404, detail="No characters found for this user"
        #    )
    except BadRequestException as e:
        raise e
    except Exception as error:
        raise InternalServerErrorException()

@function_log
@char_route.get(path="/char-list/{character_id}/archetypes")
async def get_archetypes(character_id: int):
    """
        Получение архтипов персонажа.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    character = new_db_source.get_by_id("character_list", character_id)
    if character == []:
        return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
    character = character[0]              
    level_info  = new_db_source.get_by_value("levels_capabilities","character_class",character["character_class"])[0]
    levels = [3,7,11,15,18]
    if character["lvl"] in levels:
        choose_stats = True
    if character["lvl"] == level_info["lvl_to_choose_archetype"] - 1:
        archetypes = list(level_info["archetypes"].keys()) 
    return {"archetypes": archetypes,"choose_stats" : choose_stats}