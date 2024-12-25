from fastapi import APIRouter, HTTPException
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
    BadRequestException,
    InternalServerErrorException,
    ServiceUnavailableException
)

char_route = APIRouter(prefix="/characters", tags=["characters"])



@char_route.post(path="/char-list", response_model=CharListRequestModel)
def add_character(character: CharListRequestModel):
    try:
        if not character:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        new_character = character.model_dump(exclude_unset=True)
        result = new_db_source.insert("character_list", new_character)
        if result:
            return result
        else:
            raise ServiceUnavailableException()
    except BadRequestException as e:
        raise e
    except Exception as error:
        print(error)
        raise InternalServerErrorException()


@char_route.put(path="/char-list", response_model=CharListRequestModel)
def update_character(character_id: int, character: CharListRequestModel):
    try:
        if not character_id or not character:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        updated_character = character.model_dump(exclude_unset=True)
        result = new_db_source.update("character_list", updated_character, character_id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except BadRequestException as e:
        raise e
    except Exception as error:
        print(error)
        raise InternalServerErrorException()


@char_route.get(path="/char-list/{character_id}")
def get_character(character_id: int):
    try:
        if not character_id:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character:
            return character
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except BadRequestException as e:
        raise e
    except Exception as error:
        print(error)
        raise InternalServerErrorException()


@char_route.delete(path="/char-list/{character_id}")
def delete_character(character_id: int):
    try:
        if not character_id:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character:
            new_db_source.delete("character_list", character_id)
            return {"detail": "Character deleted successfully", "character": character}
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except BadRequestException as e:
        raise e
    except Exception as error:
        print(error)
        raise InternalServerErrorException()


@char_route.get(path="/char-list/{user_id}/")
def get_characters_by_user(user_id: str):
    try:
        if not user_id:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        characters = new_db_source.get_by_value("character_list", "user_id", user_id)
        if characters:
            return characters
        else:
            raise HTTPException(
                status_code=404, detail="No characters found for this user"
            )
    except BadRequestException as e:
        raise e
    except Exception as error:
        print(error)
        raise InternalServerErrorException()