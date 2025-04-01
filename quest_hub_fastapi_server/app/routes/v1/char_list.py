import uuid
import math
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
    Note,Item,LevelUp,
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
async def update_character(character_id: uuid.UUID|str, character: CharListRequestModel):
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
async def get_character(character_id: uuid.UUID|str):
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
async def delete_character(character_id: uuid.UUID|str):
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
    
@char_route.get(path="/char-list/{character_id}/archetypes")
async def get_archetypes(character_id: int):
    """
        Получение архтипов персонажа.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    character = new_db_source.get_by_id("character_list", character_id)
    if character == []:
        return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
    character = character[0]              
    level_info  = new_db_source.get_by_value("levels_capabilities","character_class",character["character_class"])[0]
    levels = [3,7,11,15,18]
    if character["lvl"] in levels:
        choose_stats = True
    if character["lvl"] == level_info["lvl_to_choose_archetype"] - 1:
        archetypes = list(level_info["archetypes"].keys()) 
    return {"archetypes": archetypes,"choose_stats" : choose_stats}


# @char_route.put(path="/char-list/{character_id}/level_up")
# async def level_up(character_id: int,level_up:LevelUp):
#     """
#         Повышение уровня персонажа.
#     """
#     archetype = level_up.archetype
#     stats = level_up.stats
#     new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
#     new_db_source.connect()
#     character = new_db_source.get_by_id("character_list", character_id)
#     if character == []:
#         return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
#     character = character[0]
#     print(character)
#     level_info  = new_db_source.get_by_value("levels_capabilities","character_class",character["character_class"])[0]
#     character["lvl"] += 1
#     character["hp"] = level_info["health_formula"] + character["stat_modifiers"]["constitution"] * character["lvl"] + (level_info["health_formula"]//2 + 1) * (character["lvl"] - 1)
#     character["ownership_bonus"] = math.ceil(character["lvl"] / 4) + 1
#     if str(character["lvl"]) in list(level_info["traits_and_abilities"].keys()):
#         abilities = level_info["traits_and_abilities"][str(character["lvl"])].split("|")
#         for ability in abilities:   
#             ability = ability.split(":")
#             character["traits_and_abilities"][ability[0]] = ability[1]
#     if level_info["lvl_to_choose_archetype"] == character["lvl"] and archetype != None:
#         character["archetype"] = archetype
#     if 4 == character["lvl"]:
#         new_db_source.insert(table_name="stats_by_level",insert_dict={"id": character_id,"updates_by_level":{}})
#     if level_info["lvl_to_choose_archetype"] == character["lvl"]: 
#         abilities = level_info["archetypes"][character["archetype"]][str(character["lvl"])].split("|")
#         for ability in abilities:   
#             ability = ability.split(":")
#             character["traits_and_abilities"][ability[0]] = ability[1]
#     levels = [4,8,12,16,19]
#     if character["lvl"] in levels and stats != None:   
#         stats_by_level = new_db_source.get_by_value("stats_by_level","id",character_id)[0]
#         #повышение одной характеристики на 2 или двух на 1
#         character["stats"][stats[0]] += 1
#         if len(stats) == 1:
#             character["stats"][stats[0]] += 1
#             stats_by_level["updates_by_level"][character["lvl"]] = stats
#         if len(stats) == 2:
#             character["stats"][stats[1]] += 1
#             stats_by_level["updates_by_level"][character["lvl"]] = stats
#         print(stats_by_level)
#         new_db_source.update("stats_by_level", stats_by_level, character_id)
#     new_db_source.update("character_list", character, character_id)
#     print(character)
#     pass

# @char_route.put(path="/char-list/{character_id}/level_down")
# async def level_down(character_id: int):
#     """
#         Понижение уровня персонажа.
#     """
#     new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
#     new_db_source.connect()
#     character = new_db_source.get_by_id("character_list", character_id)
#     if character == []:
#         return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
#     character = character[0]
#     print(character)
#     level_info  = new_db_source.get_by_value("levels_capabilities","character_class",character["character_class"])[0]
#     if str(character["lvl"]) in list(level_info["traits_and_abilities"].keys()):
#         abilities = level_info["traits_and_abilities"][str(character["lvl"])].split("|")
#         for ability in abilities:   
#             ability = ability.split(":")
#             del character["traits_and_abilities"][ability[0]]
#     if level_info["lvl_to_choose_archetype"] <= character["lvl"]:
#         if str(character["lvl"]) in list(level_info["traits_and_abilities"].keys()):
#             abilities = level_info["archetypes"][character["archetype"]][str(character["lvl"])].split("|")
#             for ability in abilities:   
#                 ability = ability.split(":")
#                 del character["traits_and_abilities"][ability[0]]
#     if level_info["lvl_to_choose_archetype"] == character["lvl"]:
#         character["archetype"] = None
#         pass  
#     levels = [4,8,12,16,19]
#     if character["lvl"] in levels:
#         stats_by_level = new_db_source.get_by_value("stats_by_level","id",character_id)[0]
#         stats = stats_by_level["updates_by_level"][str(character["lvl"])]
#         character["stats"][stats[0]] -= 1
#         if len(stats) == 1:
#             character["stats"][stats[0]] -= 1
#             stats_by_level["updates_by_level"].pop(str(character["lvl"]))
#         if len(stats) == 2:
#             character["stats"][stats[1]] -= 1
#             stats_by_level["updates_by_level"].pop(str(character["lvl"]))
#         new_db_source.update("stats_by_level", stats_by_level, character_id)
#     character["lvl"] -= 1
#     if character["lvl"] == 3:
#         new_db_source.delete("stats_by_level",character_id)
#     character["hp"] = level_info["health_formula"] + character["stat_modifiers"]["constitution"] * character["lvl"] + (level_info["health_formula"]//2 + 1) * (character["lvl"] - 1)
#     character["ownership_bonus"] = math.ceil(character["lvl"] / 4) + 1
#     new_db_source.update("character_list", character, character_id)
#     print(character)
#     pass
