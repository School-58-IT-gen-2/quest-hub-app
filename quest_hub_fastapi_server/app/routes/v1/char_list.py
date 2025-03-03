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

char_route = APIRouter(prefix="/characters", tags=["characters"])
note_route = APIRouter(prefix="/characters", tags=["notes"])
inventory_route = APIRouter(prefix="/characters", tags=["inventory"])
ammunition_route = APIRouter(prefix="/characters", tags=["ammunition"])

@char_route.post(path="/char-list", response_model=CharListRequestModel)
async def add_character(character: CharListRequestModel):
    """
        Создание персонажа.

        Args:
            character (CharListRequestModel): Данные персонажа.
        Returns:
            response (dict): Данные персонажа.
        Raises:
            BadRequestException: Некорректный запрос.
            InternalServerErrorException: Внутренняя ошибка сервера.
            ServiceUnavailableException: Сервис временно недоступен.
    """
    #try:
    if not character:
        raise BadRequestException()
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    new_character = character.model_dump(exclude_unset=True)
    result = new_db_source.insert("character_list", new_character)
    if result:
        return result[0]
    else:
        raise ServiceUnavailableException()
    #except BadRequestException as e:
    #    raise e
    #except Exception as error:
    #    raise InternalServerErrorException()


@char_route.put(path="/char-list", response_model=CharListRequestModel)
async def update_character(character_id: int, character: CharListRequestModel):
    """
        Обновление данных персонажа.

        Args:
            character_id (int): ID персонажа.
            character (CharListRequestModel): Данные персонажа.
        Returns:
            response (dict): Данные персонажа.
        Raises:
            BadRequestException: Некорректный запрос.
            InternalServerErrorException: Внутренняя ошибка сервера.
            NotFoundException: Персонаж не найден.
    """
    try:
        if not character_id or not character:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        updated_character = character.model_dump(exclude_unset=True)
        result = new_db_source.update("character_list", updated_character, character_id)
        if result:
            return result[0]
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except BadRequestException as e:
        raise e
    except Exception as error:
        raise InternalServerErrorException()


@char_route.get(path="/char-list/{character_id}")
async def get_character(character_id: int):
    """
        Получение данных персонажа по ID.
        Args:
            character_id (int): ID персонажа.
        Returns:
            response (dict): Данные персонажа.
        Raises:
            BadRequestException: Некорректный запрос.
            NotFoundException: Персонаж не найден.
            InternalServerErrorException: Внутренняя ошибка сервера.
    """
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
        raise InternalServerErrorException()


@char_route.delete(path="/char-list/{character_id}")
async def delete_character(character_id: int):
    """
        Удаление персонажа по ID.
        Args:
            character_id (int): ID персонажа.
        Returns:
            response (dict): Данные персонажа.
        Raises:
            BadRequestException: Некорректный запрос.
            NotFoundException: Персонаж не найден.
            InternalServerErrorException: Внутренняя ошибка сервера.
    """
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
        raise InternalServerErrorException()
    
@char_route.get(path="/char-list/{user_id}/")
async def get_characters_by_user(user_id: str):
    """
        Получение персонажей по ID пользователя.
        Args:
            user_id (str): ID пользователя.
        Returns:
            response (list): Список персонажей.
        Raises:
            BadRequestException: Некорректный запрос.
            NotFoundException: Персонажи не найдены.
            InternalServerErrorException: Внутренняя ошибка сервера.
    """
    try:
        if not user_id:
            raise BadRequestException()
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        characters = new_db_source.get_by_value("character_list", "user_id", user_id)
        #if characters:
        return characters
        #else:
        #    raise HTTPException(
        #        status_code=404, detail="No characters found for this user"
        #    )
    except BadRequestException as e:
        raise e
    except Exception as error:
        raise InternalServerErrorException()
    
@char_route.put(path="/char-list/{character_id}/gold")
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
    
@char_route.put(path="/char-list/{character_id}/experience")
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


@inventory_route.get(path="/{character_id}/inventory")
async def get_inventory(character_id: int, item_id: str):
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
        for i in character["inventory"]:
            if i["id"] == item_id:
                return JSONResponse(content=i, status_code=200)
        return JSONResponse(content={"message": "Предмет не найден"}, status_code=404)
    except Exception as error:
        raise InternalServerErrorException()

@inventory_route.post(path="/{character_id}/inventory")
async def add_item_to_inventory(character_id: int, item: Item):
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
        return JSONResponse(content=_item, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@inventory_route.delete(path="/{character_id}/inventory")
async def delete_item_from_inventory(character_id: int, item_id: str):
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
        return JSONResponse(content=deleted_item, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@inventory_route.put(path="/{character_id}/inventory")
async def update_item_in_inventory(character_id: int, item: Item):
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
        for i in character["inventory"]:
            if str(i["id"]) == str(item["id"]):
                i.update(item)
                break
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=item, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    

@ammunition_route.get(path="/{character_id}/ammunition")
async def get_ammunition(character_id: int, item_id: str):
    """
        Получение аммуниции персонажа.
        Args:
            character_id (int): ID персонажа.
            item_id (uuid): айди предмета для удаления из иннвентаря.
        Returns:
            response (dict): Аммуникация персонажа.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        for i in character["weapons_and_equipment"]:
            if i["id"] == item_id:
                return JSONResponse(content=i, status_code=200)
        return JSONResponse(content={"message": "Предмет не найден"}, status_code=404)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)


@ammunition_route.post(path="/char-list/{character_id}/ammunition")
async def add_item_to_ammunition(character_id: int, item: Item):
    """
        Добавление предмета в аммуницию персонажа.
        Args:
            character_id (int): ID персонажа.
            item (Item): Предмет для добавления в аммуницию.
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
        for i in character["weapons_and_equipment"]:
            if [{j:i[j]} for j in i.keys() if j not in ["id","count"]] == [{j:_item[j]} for j in _item.keys() if j not in ["id","count"]]:
                i["count"] += _item["count"]
                _is_uniq = False
                break
        if _is_uniq:
            character["weapons_and_equipment"].append(_item)
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=_item, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@ammunition_route.delete(path="/{character_id}/ammunition")
async def delete_item_from_ammunition(character_id: int, item_id: str):
    """
        Удаление предмета из аммуниции персонажа.
        Args:
            character_id (int): ID персонажа.
            item_id (uuid): айди предмета для удаления из аммуниции.
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
        deleted_item = {}
        for i in character["weapons_and_equipment"]:
            if i["id"] == item_id:
                deleted_item = i
                i["count"] -= 1
                if i["count"] <= 0:
                    character["weapons_and_equipment"].remove(i)
                break
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=deleted_item, status_code=200)
    except:
       return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@ammunition_route.put(path="/{character_id}/ammunition")
async def update_item_in_ammunition(character_id: int, item: Item):
    """
        Обновление предмета в аммуниции персонажа.
        Args:
            character_id (int): ID персонажа.
            item (Item): Предмет для обновления в аммуниции.
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
        for i in character["weapons_and_equipment"]:
            if i["id"] == item.id:
                i.update(item.model_dump())
                break
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=item.model_dump(), status_code=200)
    except:
        return JSONResponse(content={"message":"Что-то пошло не так"}, status_code=400)

@note_route.get(path="/{character_id}/notes")
async def get_notes_of_character(character_id: int, note_id: str):
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
        for i in character["notes"]:
            if i["id"] == note_id:
                return JSONResponse(content=i, status_code=200)
        return JSONResponse(content={"message": "Заметка не найдена"}, status_code=404)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)


@note_route.post(path="/{character_id}/notes")
async def add_note_to_character(character_id: int, note: Note):
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
    
@note_route.delete(path="/{character_id}/notes")
async def delete_note_from_character(character_id: int, note_id: str):
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
    
@note_route.put(path="/{character_id}/notes")
async def update_note_from_character(character_id: int, note: Note):
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
    
