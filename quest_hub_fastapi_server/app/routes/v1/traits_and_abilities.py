import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
    Note,Item,TraitsAndAbilities,
    BadRequestException,
    InternalServerErrorException,
    ServiceUnavailableException
)

traits_and_abilities_route = APIRouter(prefix="/characters",tags=["traits_and_abilities"])

@traits_and_abilities_route.get("/{character_id}/traits_and_abilities")
async def get_traits_and_abilities(character_id: uuid.UUID,trait_id: Optional[str] = None):
    """
    Получить список характеристик и способностей для персонажа.
    Args:
        character_id (uuid.UUID): Идентификатор персонажа.
        trait_id (str): Идентификатор способности.
    Returns:
        JSONResponse: Список характеристик и способностей для персонажа.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        if trait_id is None:
            return JSONResponse(content=character["traits_and_abilities"], status_code=200)
        ability = [i if i["id"] == trait_id else None for i in character["traits_and_abilities"]]
        if ability == []:
            raise HTTPException(status_code=404, detail="Не нашли способность")
        ability = ability[0]
        return JSONResponse(content=ability, status_code=200)
    except Exception as e:
        raise InternalServerErrorException(str(e))
    
@traits_and_abilities_route.post("/{character_id}/traits_and_abilities")
async def create_traits_and_abilities(character_id: uuid.UUID,traits_and_abilities: TraitsAndAbilities):
    """
    Создать характеристику или способность для персонажа.
    Args:
        character_id (uuid.UUID): Идентификатор персона.
        trait (TraitsAndAbilities): Характеристика или способность для создания.
    Returns:
        JSONResponse: Созданная характеристика или способность.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        _tnb = traits_and_abilities.model_dump()
        _tnb["id"] = str(uuid.uuid4())
        character["traits_and_abilities"].append(_tnb)
        db_source.update("character_list",character, character_id)
        return JSONResponse(content=_tnb, status_code=201)
    except Exception as e:
        raise InternalServerErrorException(str(e))
    
@traits_and_abilities_route.put("/{character_id}/traits_and_abilities")
async def update_traits_and_abilities(character_id: uuid.UUID,traits_and_abilities: TraitsAndAbilities):
    """
    Обновить характеристику или способность персонажа.
    Args:
        character_id (uuid.UUID): Идентификатор персонажа.
        trait (TraitsAndAbilities): Характеристика или способность для обновления.
    Returns:
        JSONResponse: Обновленная характеристика или способность.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        _tnb = traits_and_abilities.model_dump()
        trait_id = _tnb["id"]
        character["traits_and_abilities"] = [i if i["id"] != trait_id else _tnb for i in character["traits_and_abilities"]]
        db_source.update("character_list",character, character_id)
        return JSONResponse(content=_tnb, status_code=200)
    except:
        raise BadRequestException("Неправильный запрос")
    

@traits_and_abilities_route.delete("/{character_id}/traits_and_abilities")
async def delete_traits_and_abilities(character_id: uuid.UUID,trait_id: str):
    """
    Удалить характеристику или способность персонажа.
    Args:
        character_id (uuid.UUID): Идентификатор персонажа.
        trait_id (str): Идентификатор способности.
    Returns:
        JSONResponse: Сообщение об успешном удалении.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        ability =  [i for i in character["traits_and_abilities"] if i["id"] == str(trait_id)]
        character["traits_and_abilities"] = [i for i in character["traits_and_abilities"] if i["id"] != str(trait_id)]
        db_source.update("character_list",character, character_id)
        return JSONResponse(content=ability[0], status_code=200)
    except Exception as e:
        raise InternalServerErrorException(str(e))