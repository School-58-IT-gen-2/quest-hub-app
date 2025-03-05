import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings

exp_route = APIRouter(prefix="/characters", tags=["experience"])

@exp_route.put(path="/{character_id}/experience")
async def update_experience_from_character(character_id: int, experience: int):
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