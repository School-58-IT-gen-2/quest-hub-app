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
    try:
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
    except BadRequestException as e:
        raise e
    except Exception as error:
        print(error)
        raise InternalServerErrorException()


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
        print(error)
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
        print(error)
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
        print(error)
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
        print(error)
        raise InternalServerErrorException()
    
@char_route.post(path="/char-list/{character_id}/inventory")
async def add_item_to_inventory(character_id: int, item: Item):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        for i in item.items:
            character["inventory"].append(i)
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"message": "Предмет добавлен в инвентарь"}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.delete(path="/char-list/{character_id}/inventory")
async def delete_item_from_inventory(character_id: int, item: Item):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        for i in item.items:
            character["inventory"].remove(i)
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"message": "Предмет удален из инвентаря"}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.put(path="/char-list/{character_id}/inventory")
async def update_item_in_inventory(character_id: int, item: Item):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.post(path="/char-list/{character_id}/ammunition")
async def add_item_to_ammunition(character_id: int, item: Item):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        character["weapons_and_equipmrnt"] = {**character["weapons_and_equipmrnt"], **item.ammunition_items}
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"message": "Добавлен предмет в аммуницию"}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.delete(path="/char-list/{character_id}/ammunition")
async def delete_item_from_ammunition(character_id: int, item: Item):
    try:
        pass # потом допишу
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.put(path="/char-list/{character_id}/ammunition")
async def update_item_in_ammunition(character_id: int, item: Item):
    try:
        pass # потом допишу
    except:
        return JSONResponse(content={"message":"Что-то пошло не так"}, status_code=400)

@char_route.post(path="/char-list/{character_id}/notes")
async def add_note_to_character(character_id: int, note: Note):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        if character["notes"] == None:
            character["notes"] = note.note
        else:
            character["notes"] = {**character["notes"], **note.note}
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"message": "Добавлена заметка"}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.delete(path="/char-list/{character_id}/notes")
async def delete_note_from_character(character_id: int, note: Note):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        try:
            for i in note.note.keys():
                character["notes"].pop(i)
        except:
            pass
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"message": "Заметка удалена"}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.put(path="/char-list/{character_id}/notes")
async def update_note_from_character(character_id: int, note: Note):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        try:
            for i in note.note.keys():
                character["notes"][i] = note.note[i]
        except:
            pass
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"message": "Заметка обновлена"}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.put(path="/char-list/{character_id}/gold")
async def update_gold_from_character(character_id: int, gold: str):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        if "+" in gold:
            character["gold"] += int(gold.split("+")[1])
        if "-" in gold:
            character["gold"] -= int(gold.split("-")[1])
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"message": "Золото обновлено"}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.put(path="/char-list/{character_id}/experience")
async def update_experience_from_character(character_id: int, experience: str):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character == []:
            return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
        character = character[0]
        if "+" in experience:
            character["experience"] += int(experience.split("+")[1])
        if "-" in experience:
            character["experience"] -= int(experience.split("-")[1])
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content={"message": "Золото обновлено"}, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)