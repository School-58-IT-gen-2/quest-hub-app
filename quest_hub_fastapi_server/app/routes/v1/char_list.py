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
from logs.log import function_log

char_route = APIRouter(prefix="/characters", tags=["characters"])

@function_log
@char_route.post(path="/char-list", response_model=CharListRequestModel)
async def add_character(character: CharListRequestModel):
    try:
        if not character:
            raise BadRequestException()
            
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        
        new_character = character.model_dump(exclude_unset=True)
        
        new_db_source.insert("character_list", new_character)
        
        if character.id:
            fetched_character = new_db_source.get_by_id("character_list", character.id)
            if fetched_character and isinstance(fetched_character, list) and len(fetched_character) > 0:
                return CharListRequestModel(**fetched_character[0])
        
        return character
        
    except BadRequestException as e:
        raise e
    except Exception as error:
        print(f"Error creating character: {error}")
        raise InternalServerErrorException()



@function_log
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


@function_log
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


@function_log
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


@function_log
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
async def get_data_to_choose(character_id: str):
    """
        Получение архетипов и необходимости выбора характеристик.
    """
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    character = new_db_source.get_by_id("character_list", character_id)
    if not character:
        return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
    character = character[0]
    level_data = new_db_source.get_by_value("levels_capabilities", "character_class", character["character_class"])
    if not level_data:
        raise HTTPException(
            status_code=404,
            detail=f"Для класса '{character['character_class']}' не найдены уровни способностей"
        )
    level_info = level_data[0]
    archetypes = []
    choose_stats = False
    if character["lvl"] == level_info["lvl_to_choose_archetype"] - 1:
        archetypes = list(level_info["archetypes"].keys())
    if character["lvl"] in [4, 8, 12, 16, 19]:
        choose_stats = True

    return {"archetypes": archetypes, "choose_stats": choose_stats}

@char_route.put(path="/char-list/{character_id}/level_up")
async def level_up(character_id: str, level_up: LevelUp):
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()

    character = new_db_source.get_by_id("character_list", character_id)
    if not character:
        return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
    character = character[0]
    level_info = new_db_source.get_by_value("levels_capabilities", "character_class", character["character_class"])[0]
    if isinstance(character["traits_and_abilities"], list):
        traits_dict = {}
    for trait in character["traits_and_abilities"]:
        traits_dict[trait["name"]] = trait["description"]
    character["traits_and_abilities"] = traits_dict

    character["lvl"] += 1

    # Увеличение хитов (учитывая базовую формулу)
    character["hp"] = level_info["health_formula"] + character["stat_modifiers"]["constitution"] * character["lvl"] + (level_info["health_formula"] // 2 + 1) * (character["lvl"] - 1)

    # Обновляем бонус мастерства
    character["ownership_bonus"] = math.ceil(character["lvl"] / 4) + 1

    # Добавление/обновление умений на этом уровне
    lvl_str = str(character["lvl"])
    if lvl_str in level_info["traits_and_abilities"]:
        for ability in level_info["traits_and_abilities"][lvl_str].split("|"):
            name, desc = ability.split(":", 1)
            character["traits_and_abilities"][name] = desc

    # Архетип
    if character["lvl"] == level_info["lvl_to_choose_archetype"] and level_up.archetype:
        character["archetype"] = level_up.archetype

    # Умения архетипа
    if character["archetype"] and lvl_str in level_info["archetypes"][character["archetype"]]:
        for ability in level_info["archetypes"][character["archetype"]][lvl_str].split("|"):
            name, desc = ability.split(":", 1)
            character["traits_and_abilities"][name] = desc

    # Повышение характеристик
    if character["lvl"] in [4, 8, 12, 16, 19] and level_up.stats:
        stats_by_level = new_db_source.get_by_value("stats_by_level", "id", character_id)
        if not stats_by_level:
            stats_by_level = {"id": character_id, "updates_by_level": {}}
        else:
            stats_by_level = stats_by_level[0]

        stats = level_up.stats
        character["stats"][stats[0]] += 1
        if len(stats) == 1:
            character["stats"][stats[0]] += 1
        elif len(stats) == 2:
            character["stats"][stats[1]] += 1

        stats_by_level["updates_by_level"][character["lvl"]] = stats
        new_db_source.update("stats_by_level", stats_by_level, character_id)
    new_db_source.update("character_list", character, character_id)
    return character
@char_route.put(path="/char-list/{character_id}/level_down")
async def level_down(character_id: str):
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()

    character = new_db_source.get_by_id("character_list", character_id)
    if isinstance(character["traits_and_abilities"], list):
        traits_dict = {}
    for trait in character["traits_and_abilities"]:
        traits_dict[trait["name"]] = trait["description"]
    character["traits_and_abilities"] = traits_dict
    if not character:
        return JSONResponse(content={"message": "Персонаж не найден"}, status_code=404)
    character = character[0]
    level_info = new_db_source.get_by_value("levels_capabilities", "character_class", character["character_class"])[0]

    lvl_str = str(character["lvl"])

    # Удаление способностей текущего уровня (или откат до более ранней версии)
    if lvl_str in level_info["traits_and_abilities"]:
        for ability in level_info["traits_and_abilities"][lvl_str].split("|"):
            name, _ = ability.split(":", 1)
            found = False
            for lvl in range(character["lvl"] - 1, 0, -1):
                prev_lvl_str = str(lvl)
                if prev_lvl_str in level_info["traits_and_abilities"]:
                    for prev_ability in level_info["traits_and_abilities"][prev_lvl_str].split("|"):
                        prev_name, prev_desc = prev_ability.split(":", 1)
                        if prev_name == name:
                            character["traits_and_abilities"][name] = prev_desc
                            found = True
                            break
                if found:
                    break
            if not found and name in character["traits_and_abilities"]:
                del character["traits_and_abilities"][name]

    # Архетип
    if character["archetype"] and lvl_str in level_info["archetypes"].get(character["archetype"], {}):
        for ability in level_info["archetypes"][character["archetype"]][lvl_str].split("|"):
            name, _ = ability.split(":", 1)
            del character["traits_and_abilities"][name]

    if character["lvl"] == level_info["lvl_to_choose_archetype"]:
        character["archetype"] = None

    # Понижение характеристик
    if character["lvl"] in [4, 8, 12, 16, 19]:
        stats_by_level = new_db_source.get_by_value("stats_by_level", "id", character_id)[0]
        stats = stats_by_level["updates_by_level"].pop(str(character["lvl"]))
        character["stats"][stats[0]] -= 1
        if len(stats) == 1:
            character["stats"][stats[0]] -= 1
        else:
            character["stats"][stats[1]] -= 1
        new_db_source.update("stats_by_level", stats_by_level, character_id)

    character["lvl"] -= 1


    # Перерасчёт хитов и бонуса мастерства
    character["hp"] = level_info["health_formula"] + character["stat_modifiers"]["constitution"] * character["lvl"] + (level_info["health_formula"] // 2 + 1) * (character["lvl"] - 1)
    character["ownership_bonus"] = math.ceil(character["lvl"] / 4) + 1

    new_db_source.update("character_list", character, character_id)
    return character