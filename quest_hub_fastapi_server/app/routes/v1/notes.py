import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
    Note,Item,
    BadRequestException,
    InternalServerErrorException,
    ServiceUnavailableException
)

from logs.log import function_log

note_route = APIRouter(prefix="/characters", tags=["notes"])


# @function_log
@note_route.get(path="/{character_id}/notes")
async def get_notes_of_character(character_id: uuid.UUID|str, note_id: Optional[str] = None):
    """
        Получение заметок персонажа.
        Args:
            character_id (int): ID персонажа.
            note_id (str): ID заметки.
        Returns:
            response (dict): Заметка персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        if note_id is None:
            return JSONResponse(content=character["notes"], status_code=200)
        for i in character["notes"]:
            if i["id"] == note_id:
                return JSONResponse(content=i, status_code=200)
        return JSONResponse(content={"message": "Заметка не найдена"}, status_code=404)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)

# @function_log
@note_route.post(path="/{character_id}/notes")
async def add_note_to_character(character_id: uuid.UUID|str, note: Note):
    """
        Добавление заметки к персонажу.
        Args:
            character_id (int): ID персонажа.
            note (Note): Заметка для добавления.
        Returns:
            response (dict): Добавленная заметка.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        if note.title == None and note.text == None:
            return JSONResponse(content={"message": "Заметка не может быть пустой"}, status_code=400)
        new_note = note.model_dump()
        new_note["id"] = str(uuid.uuid4())
        if character["notes"] == None:
            character["notes"] = []
        character["notes"].append(new_note)
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=new_note, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)

# @function_log
@note_route.delete(path="/{character_id}/notes")
async def delete_note_from_character(character_id: uuid.UUID|str, note_id: str):
    """
        Удаление заметки у персонажа.
        Args:
            character_id (int): ID персонажа.
            notee_id (uuid/str): ID заметки для удаления.
        Returns:
            response (dict): Удаленная заметка.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        note = [i for i in character["notes"] if i["id"] == note_id][0]
        character["notes"] = [i for i in character["notes"] if i["id"] != note_id]
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=note, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)

# @function_log
@note_route.put(path="/{character_id}/notes")
async def update_note_from_character(character_id: uuid.UUID|str, note: Note):
    """
        Обновление заметки у персонажа.
        Args:
            character_id (int): ID персонажа.
            note (Note): Заметка для обновления.
        Returns:
            response (dict): Обновленная заметка.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        if note.id == None:
            return JSONResponse(content={"message": "ID заметки не указан"}, status_code=400)
        if note.title == None and note.text == None:
            return JSONResponse(content={"message": "Заметка не может быть пустой"}, status_code=400)
        new_note = {}
        for i in character["notes"]:
            if str(i["id"]) == str(note.id):
                i["text"] = note.text if note.text != None else i["text"]
                i["title"] = note.title if note.title != None else i["title"]
                new_note = i
                break
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=new_note, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)