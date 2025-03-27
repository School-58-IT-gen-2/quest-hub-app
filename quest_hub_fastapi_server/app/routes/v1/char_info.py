import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import *

char_info_route = APIRouter(prefix="/characters", tags=["character information"])

@char_info_route.put(path="/{character_id}/name")
async def update_character_name(character_id: uuid.UUID|str, update: UpdateCharacterName):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["name"] = update.new_name
        result = new_db_source.update("character_list", character, character_id)
        if result:
            return JSONResponse(content={"new_name": update.new_name})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
        raise InternalServerErrorException()

@char_info_route.put(path="/{character_id}/surname")
async def update_character_surname(character_id: uuid.UUID|str, update: UpdateCharacterSurname):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["surname"] = update.new_surname
        result = new_db_source.update("character_list", character, character_id)
        if result:
            return JSONResponse(content={"new_surname": update.new_surname})
        else:
            raise ServiceUnavailableException()
    except:
        raise InternalServerErrorException()

@char_info_route.put(path="/{character_id}/age")
async def update_character_age(character_id: uuid.UUID|str, update: UpdateCharacterAge):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["age"] = update.new_age
        result = new_db_source.update("character_list", character, character_id)
        if result:
            return JSONResponse(content={"new_age": update.new_age})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
        raise InternalServerErrorException()

@char_info_route.put(path="/{character_id}/backstory")
async def update_character_backstory(character_id: uuid.UUID|str, update: UpdateCharacterBackstory):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["backstory"] = update.new_backstory
        result = new_db_source.update("character_list", character, character_id)
        if result:
            return JSONResponse(content={"new_backstory": update.new_backstory})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
        raise InternalServerErrorException()

@char_info_route.post(path="/{character_id}/languages")
async def add_character_language(character_id: uuid.UUID|str, update: AddCharacterLanguage):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        character["languages"].append(update.language)
        result = new_db_source.update("character_list", character, character_id)
        if result:
            return JSONResponse(content={"new_language": update.language})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
        raise InternalServerErrorException()

@char_info_route.delete(path="/{character_id}/languages")
async def delete_character_language(character_id: uuid.UUID|str, update: DeleteCharacterLanguage):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Нету такого персонажа")
        character = character[0]
        try:
            character["languages"].remove(update.language)
        except:
            raise HTTPException(status_code=404, detail="Нету такого языка")
        result = new_db_source.update("character_list", character, character_id)
        if result:
            return JSONResponse(content={"removed_languages": update.language})
        else:
            raise ServiceUnavailableException()
    except Exception as error:
        raise InternalServerErrorException()

@char_info_route.put(path="/{character_id}/experience")
async def update_experience_from_character(character_id: uuid.UUID|str, update: UpdateExperience):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        character["experience"] += update.experience
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"new_exp": character["experience"]}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)

@char_info_route.put(path="/{character_id}/gold")
async def update_gold_from_character(character_id: uuid.UUID|str, update: UpdateGold):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        character["gold"] += update.gold
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"updated_gold": character["gold"]}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
