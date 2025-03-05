import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings


gold_route = APIRouter(prefix="/characters", tags=["gold"])

@gold_route.put(path="/{character_id}/gold")
async def update_gold_from_character(character_id: int, gold: int):
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