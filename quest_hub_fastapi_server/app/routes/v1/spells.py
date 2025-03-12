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

spell_route = APIRouter(prefix="/characters",tags=["spell"])

@spell_route.get("/{character_id}/spells")
async def get_spells(character_id: uuid.UUID,spell_id: str):
    """
    Получить заклинание персонажа."
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        spell = [i if i["id"] == spell_id else None for i in character["spells"]]
        if spell == []:
            raise HTTPException(status_code=404, detail="Не нашли заклинание")
        return JSONResponse(content=spell[0], status_code=200)
    except Exception as e:
        raise InternalServerErrorException(str(e))