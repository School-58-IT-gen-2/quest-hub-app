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
        character["inventory"].append(item.model_dump())
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=item.model_dump(), status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.delete(path="/char-list/{character_id}/inventory")
async def delete_item_from_inventory(character_id: int, item: Item):
    """
        Удаление предмета из инвентаря персонажа.
        Args:
            character_id (int): ID персонажа.
            item (Item): Предмет для удаления из инвентаря.
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
        character["inventory"] = [i for i in character["inventory"] if i["name"] != item.name]
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=item.model_dump(), status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.put(path="/char-list/{character_id}/inventory")
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
        character["inventory"] = [item.model_dump() if i["name"] == item.name else i for i in character["inventory"]]
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=item.model_dump(), status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.post(path="/char-list/{character_id}/ammunition")
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
        character["weapons_and_equipment"].append(item.model_dump())
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=item.model_dump(), status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.delete(path="/char-list/{character_id}/ammunition")
async def delete_item_from_ammunition(character_id: int, item: Item):
    """
        Удаление предмета из аммуниции персонажа.
        Args:
            character_id (int): ID персонажа.
            item (Item): Предмет для удаления из аммуниции.
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
        character["weapons_and_equipment"] = [i for i in character["weapons_and_equipment"] if i["name"] != item.name]
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=item.model_dump(), status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.put(path="/char-list/{character_id}/ammunition")
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
        character["weapons_and_equipment"] = [item.model_dump() if i["name"] == item.name else i for i in character["weapons_and_equipment"]]
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=item.model_dump(), status_code=200)
    except:
        return JSONResponse(content={"message":"Что-то пошло не так"}, status_code=400)

@char_route.post(path="/char-list/{character_id}/notes")
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
        new_note = note.model_dump()
        new_note["id"] = str(uuid.uuid4())
        character["notes"].append(new_note)
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=new_note, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.delete(path="/char-list/{character_id}/notes")
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
    
@char_route.put(path="/char-list/{character_id}/notes")
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
        #new_note = [i for i in character["notes"] if i["id"] == note.id][0]
        new_note = {}
        for i in character["notes"]:
            if str(i["id"]) == str(note.id):
                i["text"] = note.text
                i["title"] = note.title
                new_note = i
                break
        new_db_source.update("character_list", character, character_id)
        return JSONResponse(content=new_note, status_code=200)
    except:
        return JSONResponse(content={"message": "Что-то пошло не так"}, status_code=400)
    
@char_route.put(path="/char-list/{character_id}/gold")
async def update_gold_from_character(character_id: int, gold: int):
    """
        Обновление золота у персонажа.
        Args:
            character_id (int): ID персонажа.
            gold (int): Количество золота для обновления.
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
            experience (int): Количество опыта для обновления.
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
    
@char_route.put(path="/char-list/{character_id}/level_up")
async def update_experience_from_character(character_id: int):
    """
        Повышение уровня персонажа.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    character = new_db_source.get_by_id("character_list", character_id)
    if character == []:
        return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
    character = character[0]
    level_info  = new_db_source.get_by_value("levels_capabilities","character_class",character["character_class"])
    character["lvl"] += 1
    character["hp"] = level_info["health_formula"] + character["stat_modifiers"]["constitution"] * character["lvl"] + (level_info["health_formula"]//2 + 1) * (character["lvl"] - 1)
    character["ownership_bonus"] = character["lvl"] //  4 + 1
    if str(character["lvl"]) in list(level_info["traits_and_abilities"].keys()):
        abilities = level_info["traits_and_abilities"][str(character["lvl"])].split("|")
        for ability in abilities:   
            ability = ability.split(":")
            character["traits_and_abilities"][ability[0]] = ability[1]
    if level_info["lvl_to_choose_archetype"] == character["lvl"]:
        #Выбор архетипа
        pass
    if level_info["lvl_to_choose_archetype"] >= character["lvl"]:
        if str(character["lvl"]) in list(level_info["traits_and_abilities"].keys()):
            #нужен архетип,но пока не знаю,откуда его брать 
            abilities = level_info["archetypes"]["archetype"][str(character["lvl"])].split("|")
            for ability in abilities:   
                ability = ability.split(":")
                character["traits_and_abilities"][ability[0]] = ability[1]
    pass

@char_route.put(path="/char-list/{character_id}/level_down")
async def update_experience_from_character(character_id: int):
    """
        Понижение уровня персонажа.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    character = new_db_source.get_by_id("character_list", character_id)
    if character == []:
        return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
    character = character[0]
    level_info  = new_db_source.get_by_value("levels_capabilities","character_class",character["character_class"])
    if str(character["lvl"]) in list(level_info["traits_and_abilities"].keys()):
        abilities = level_info["traits_and_abilities"][str(character["lvl"])].split("|")
        for ability in abilities:   
            ability = ability.split(":")
            del character["traits_and_abilities"][ability[0]]
    if level_info["lvl_to_choose_archetype"] >= character["lvl"]:
        if str(character["lvl"]) in list(level_info["traits_and_abilities"].keys()):
            #нужен архетип,но пока не знаю,откуда его брать 
            abilities = level_info["archetypes"]["archetype"][str(character["lvl"])].split("|")
            for ability in abilities:   
                ability = ability.split(":")
                del character["traits_and_abilities"][ability[0]]
    if level_info["lvl_to_choose_archetype"] == character["lvl"]:
        #удаление архетипа
        pass  
    character["lvl"] -= 1
    character["hp"] = level_info["health_formula"] + character["stat_modifiers"]["constitution"] * character["lvl"] + (level_info["health_formula"]//2 + 1) * (character["lvl"] - 1)
    character["ownership_bonus"] = character["lvl"] //  4 + 1

    pass