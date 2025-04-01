import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
    Note,Item,Spell,
    BadRequestException,
    InternalServerErrorException,
    ServiceUnavailableException
)

from logs.log import function_log

spell_route = APIRouter(prefix="/characters",tags=["spell"])

# @function_log
@spell_route.get("/{character_id}/spells")
async def get_spells(character_id: uuid.UUID,spell_id: Optional[str] = None):
    """
    Получить заклинание персонажа.
    Args:
        character_id (uuid.UUID): Идентификатор персонажа.
        spell_id (str): Идентификатор заклинания.
    Returns:
        JSONResponse: Заклинание персонажа.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        if spell_id is None:
            return JSONResponse(content=character["spells"], status_code=200)
        spell = [i if i["id"] == spell_id else None for i in character["spells"]]
        if spell == []:
            raise HTTPException(status_code=404, detail="Не нашли заклинание")
        return JSONResponse(content=spell[0], status_code=200)
    except Exception as e:
        raise InternalServerErrorException(str(e))

# @function_log
@spell_route.post("/{character_id}/spells")
async def create_spell(character_id: uuid.UUID,spell: Spell):
    """
    Создать заклинание для персонажа.
    Args:
        character_id (uuid.UUID): Идентификатор персонажа.
        spell (Spell): Заклинание для создания.
    Returns:
        JSONResponse: Созданное заклинание.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        if character["spells"] == None:
            character["spells"] = []
        spl = spell.model_dump()
        spl["id"] = str(uuid.uuid4())
        character["spells"].append(spl)
        db_source.update("character_list",character,character_id)
        return JSONResponse(content=spl, status_code=200)
    except Exception as e:
        raise InternalServerErrorException(str(e))

# @function_log
@spell_route.put("/{character_id}/spells")
async def update_spell(character_id: uuid.UUID,spell: Spell):
    """
    Обновить заклинание персонажа.
    Args:
        character_id (uuid.UUID): Идентификатор персонажа.
        spell (Spell): Заклинание для обновления.
    Returns:
        JSONResponse: Обновленное заклинание.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        if character["spells"] == None:
            character["spells"] = []
        _spell = spell.model_dump()
        spell_id = str(_spell["id"])
        character["spells"] = [i if i["id"] != str(spell_id) else _spell for i in character["spells"]]
        db_source.update("character_list",character,character_id)
        return JSONResponse(content=_spell, status_code=200)
    except Exception as e:
        raise InternalServerErrorException(str(e))
    
# @function_log
@spell_route.delete("/{character_id}/spells")
async def delete_spell(character_id: uuid.UUID,spell_id: str):
    """
    Удалить заклинание персонажа.
    Args:
        character_id (uuid.UUID): Идентификатор персонажа.
        spell_id (str): Идентификатор заклинания.
    Returns:
        JSONResponse: Удаленное заклинание.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        if character["spells"] == None:
            character["spells"] = []
        n1 = len(character["spells"])
        _spell = [i for i in character["spells"] if i["id"] == str(spell_id)]
        character["spells"] = [i for i in character["spells"] if i["id"] != str(spell_id)]
        if n1 == len(character["spells"]):
            return JSONResponse(content="Не нашли твой спелл дибильный", status_code=404)
        if len(_spell) == 0:
            return JSONResponse(content="Не нашли твой спелл дибильный", status_code=404)
        _spell = _spell[0]
        _spell["id"] = str(uuid.uuid4())
        db_source.update("character_list",character,character_id)
        return JSONResponse(content=_spell, status_code=200)
    except Exception as e:
        raise InternalServerErrorException(str(e))