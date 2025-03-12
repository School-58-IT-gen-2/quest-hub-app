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

char_info_route = APIRouter(prefix="/characters", tags=["character information"])

@char_info_route.put(path="/{character_id}/name")
async def update_character_name(character_id: uuid.UUID|str, new_name: str):
    """
        Обновление имени персонажа.

        Args:
            character_id (int): Идентификатор персонажа.
            new_name (str): Новое имя персонажа.
        Returns:
            response (dict): Данные персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["name"] = new_name
        result = new_db_source.update("character_list",character, character_id)
        if result:
            return JSONResponse(content={"new_name": new_name})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
        raise InternalServerErrorException()

@char_info_route.put(path="/{character_id}/surname")
async def update_character_surname(character_id: uuid.UUID|str, new_surname: str):
    """
        Обновление фамилии персонажа.
        Args:
            character_id (int): Идентификатор персонажа.
            new_surname (str): Новая фамилия персонажа.
        Returns:
            response (dict): Данные персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["surname"] = new_surname
        result = new_db_source.update("character_list",character, character_id)
        if result:
            return JSONResponse(content={"new_surname": new_surname})
        else:
            raise ServiceUnavailableException()
    except:
        raise InternalServerErrorException()

@char_info_route.put(path="/{character_id}/age")
async def update_character_age(character_id: uuid.UUID|str, new_age: int):
    """
        Обновление возраста персонажа.
        Args:
            character_id (int): Идентификатор персонажа.
            new_age (int): Новый возраст персонажа.
        Returns:
            response (dict): Данные персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["age"] = new_age
        result = new_db_source.update("character_list",character, character_id)
        if result:
            return JSONResponse(content={"new_age": new_age})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
            raise InternalServerErrorException()
    
@char_info_route.put(path="/{character_id}/backstory")
async def update_character_backstory(character_id: uuid.UUID|str, new_backstory: str):
    """
        Обновление биографии персонажа.
        Args:
            character_id (int): Идентификатор персонажа.
            new_backstory (str): Новая биография персонажа.
        Returns:
            response (dict): Данные персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["backstory"] = new_backstory
        result = new_db_source.update("character_list",character, character_id)
        if result:
            return JSONResponse(content={"new_backstory": new_backstory})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
            raise InternalServerErrorException()
    
@char_info_route.post(path="/{character_id}/languages")
async def add_character_language(character_id: uuid.UUID|str, language: str):
    """
        Добавление языка персонажа.
        Args:
            character_id (int): Идентификатор персонажа.
            language (str): Язык персонажа.
        Returns:
            response (dict): Данные персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["languages"].append(language)
        result = new_db_source.update("character_list",character, character_id)
        if result:
            return JSONResponse(content={"new_language": language})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
            raise InternalServerErrorException()
    
@char_info_route.delete(path="/{character_id}/languages")
async def delete_character_language(character_id: uuid.UUID|str, language: str):
    """
        Удаление языка персонажа.
        Args:
            character_id (int): Идентификатор персонажа.
            language (str): Язык персонажа.
        Returns:
            response (dict): Данные персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        try:
            character["languages"].remove(language)
        except:
            raise HTTPException(status_code=404, detail="Нету такого языка")
        result = new_db_source.update("character_list",character, character_id)
        if result:
            return JSONResponse(content={"removed_languages": language})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
            raise InternalServerErrorException()
    
@char_info_route.put(path="/{character_id}/experience")
async def update_experience_from_character(character_id: uuid.UUID|str, experience: int):
    """
        Обновление опыта у персонажа.
        Args:
            character_id (int): ID персонажа.
            experience (int): Количество опыта для обновления (+100 или -200, например ).
        Returns:
            response (dict): Обновленное количество опыта.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        character["experience"] += experience
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"new_exp": character["experience"]}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_info_route.put(path="/{character_id}/gold")
async def update_gold_from_character(character_id: uuid.UUID|str, gold: int):
    """
        Обновление золота у персонажа.
        Args:
            character_id (int): ID персонажа.
            gold (int): Количество золота для обновления (+200 или -100, например).
        Returns:
            response (dict): Обновленное количество золота.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        character["gold"] += gold
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"updated_gold": character["gold"]}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)