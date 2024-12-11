from fastapi import APIRouter, HTTPException
from model.character_list_model import CharacterList
from adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from model.request_model.charlist_model import CharListRequestModel
route = APIRouter(prefix="/characters", tags=["characters"])


@route.post(path="/create-character", response_model=CharListRequestModel)
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


@route.put(path="/update-character/{character_id}", response_model=CharListRequestModel)
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

@route.get(path="/get-character/{character_id}")
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

@route.delete(path="/delete-character/{character_id}")
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
    

@route.get(path="/get-characters-by-user/{user_id}")
def get_characters_by_user(user_id: str):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        characters = new_db_source.get_by_value("character_list", "user_id", user_id) 
        if characters:
            return characters 
        else:
            raise HTTPException(status_code=404, detail="No characters found for this user")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error retrieving characters")