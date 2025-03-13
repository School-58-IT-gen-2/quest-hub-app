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

inventory_route = APIRouter(prefix="/characters", tags=["inventory"])

@inventory_route.get(path="/{character_id}/inventory")
async def get_inventory(character_id: uuid.UUID|str, item_id: Optional[str] = None):
    """
        Получение инвентаря персонажа.
        Args:
            character_id (int): ID персонажа.
            item_id (uuid): ID предмета.
        Returns:
            response (dict): Инвентарь персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        if item_id is None:
            return JSONResponse(content=character["inventory"], status_code=200)
        for i in character["inventory"]:
            if str(i["id"]) == str(item_id):
                res = i.copy()
                res = {j: res[j] for j in res if res[j] is not None}
                return JSONResponse(content=res, status_code=200)
        return JSONResponse(content={"message": "Предмет не найден"}, status_code=404)
    except Exception as error:
        raise InternalServerErrorException()

@inventory_route.post(path="/{character_id}/inventory")
async def add_item_to_inventory(character_id: uuid.UUID|str, item: Item):
    """
        Добавление предмета в инвентарь персонажа.
        Args:
            character_id (int): ID персонажа.
                item (Item): Предмет для добавления в инвентарь.
        Returns:
            response (dict): Добавленный предмет.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        _item = item.model_dump()
        if item.name == None:
            return JSONResponse(content={"message": "Нет названия предмета"}, status_code=400)
        _item["id"] = str(uuid.uuid4())
        _is_uniq = True
        for i in character["inventory"]:
            if [{j:i[j]} for j in i.keys() if j not in ["id","count"]] == [{j:_item[j]} for j in _item.keys() if j not in ["id","count"]]:
                i["count"] += _item["count"]
                _is_uniq = False
                break
        if _is_uniq:
            character["inventory"].append(_item)
        new_db_source.update("character_list", character, character_id)
        _item = {j: _item[j] for j in _item if _item[j] is not None}
        return JSONResponse(content=_item, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@inventory_route.delete(path="/{character_id}/inventory")
async def delete_item_from_inventory(character_id: uuid.UUID|str, item_id: str):
    """
        Удаление предмета из инвентаря персонажа.
        Args:
            character_id (int): ID персонажа.
            item_id (uuid): айди предмета для удаления из иннвентаря.
        Returns:
            response (dict): Удаленный предмет.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        for i in character["inventory"]:
            if i["id"] == item_id:
                deleted_item = i
                i["count"] -= 1
                if i["count"] <= 0:
                    character["inventory"].remove(i)
                break
        if item_id not in [i["id"] for i in character["inventory"]]:
            return JSONResponse(content={"message": "Предмет не найден"}, status_code=404)
        new_db_source.update("character_list", character, character_id)
        deleted_item = {j: deleted_item[j] for j in deleted_item if deleted_item[j] is not None}
        return JSONResponse(content=deleted_item, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@inventory_route.put(path="/{character_id}/inventory")
async def update_item_in_inventory(character_id: uuid.UUID|str, item: Item):
    """
        Обновление предмета в инвентаре персонажа.
        Args:
            character_id (int): ID персонажа.
            item (Item): Предмет для обновления в инвентаре.
        Returns:
            response (dict): Обновленный предмет.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        item = item.model_dump()
        res = {}
        for i in character["inventory"]:
            if str(i["id"]) == str(item["id"]):
                res = {j: item[j] for j in item if item[j] is not None}
                i.update(res)
                break
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=res, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)