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

traits_and_abilities_route = APIRouter(prefix="/characters",tags=["traits_and_abilities"])

@traits_and_abilities_route.get("/{character_id}/traits_and_abilities")
async def get_traits_and_abilities(character_id: uuid.UUID,ability_id: str):
    """
    Получить список характеристик и способностей для персонажа.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        character = db_source.get_by_id("character_list",character_id)
        if character == []:
            raise HTTPException(status_code=404, detail="Персонаж не найден")
        character = character[0]
        ability = [i if i["id"] == ability_id else None for i in character["traits_and_abilities"]]
        if ability == []:
            raise HTTPException(status_code=404, detail="Не нашли способность")
        ability = ability[0]
        return JSONResponse(content=ability, status_code=200)
    except Exception as e:
        raise InternalServerErrorException(str(e))