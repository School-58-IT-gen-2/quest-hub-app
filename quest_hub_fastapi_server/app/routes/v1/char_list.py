from fastapi import APIRouter, HTTPException

from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
)

char_route = APIRouter(tags=["characters"])


@char_route.post(path="/char-list", response_model=CharListRequestModel)
def add_character(character: CharListRequestModel):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        new_character = character.model_dump(exclude_unset=True)
        result = new_db_source.insert("character_list", new_character)
        if result:
            return result
        else:
            raise HTTPException(status_code=503, detail="Database unreachable")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error adding character")


@char_route.put(path="/char-list/{character_id}", response_model=CharListRequestModel)
def update_character(character_id: int, character: CharListRequestModel):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        updated_character = character.model_dump(exclude_unset=True)
        result = new_db_source.update("character_list", updated_character, character_id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error updating character")


@char_route.get(path="/char-list/{character_id}")
def get_character(character_id: int):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character:
            return character
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error retrieving character")


@char_route.delete(path="/char-list/{character_id}")
def delete_character(character_id: int):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character:
            new_db_source.delete("character_list", character_id)
            return {"detail": "Character deleted successfully", "character": character}
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error deleting character")


@char_route.get(path="/char-list/{user_id}")
def get_characters_by_user(user_id: str):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        characters = new_db_source.get_by_value("character_list", "user_id", user_id)
        if characters:
            return characters
        else:
            raise HTTPException(
                status_code=404, detail="No characters found for this user"
            )
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error retrieving characters")
