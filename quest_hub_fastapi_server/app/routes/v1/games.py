import uuid
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.games.models import *
from logs.log import function_log
from datetime import datetime
from string import ascii_letters, digits
import random

games_route = APIRouter(prefix="/games", tags=["games"])

def generate_seed():
    seed = []
    for i in range(6):
        t = list(ascii_letters+digits)[random.randint(0, len(ascii_letters+digits)-1)]
        seed.append(t)
    return "".join(seed)

@function_log
@games_route.post(path="/create")
async def create_game(game_data: Game):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        level = game_data.level
        if level != None:
            level = level.value
        game = game_data.model_dump()
        game.pop("id")
        game.pop("created_at")
        game["players_id"] = [str(i) for i in  game["players_id"]]
        game["master_id"] = str(game["master_id"])
        game["seed"] = generate_seed()
        game["level"] = level
        while new_db_source.get_by_value("games", "seed", game["seed"]) != []:
            game["seed"] = generate_seed()
        result = new_db_source.insert("games", game)
        if result != []:
            return JSONResponse(content=result[0],status_code=201)
        else:
            return JSONResponse(content={"error": "Ошибка при создании игры"}, status_code=500)
    except Exception as error:
        return JSONResponse(content={"error": f"{error}"}, status_code=400)
    
@function_log
@games_route.get(path="/view_game")
async def view_part_game(game_id: uuid.UUID|str):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        if game_id is None:
            games = new_db_source.get_all("games")
            return JSONResponse(content=games, status_code=200)
        else:
            game = new_db_source.get_by_id("games", game_id)
            if game == []:
                raise HTTPException(status_code=404, detail="Нету такой игры")
            return JSONResponse(content=game[0], status_code=200)
    except:
        return JSONResponse(content={"error": "Ошибка при просмотре игры"}, status_code=400)

# @function_log
# @games_route.get(path="/view_all_games")
# async def view_part_game():
#     try:
#         new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
#         new_db_source.connect()
#         games = new_db_source.get_all("games")
#         return JSONResponse(content=games, status_code=200)
#     except:
#         return JSONResponse(content={"error": "Ошибка при просмотре игры"}, status_code=400)

@function_log 
@games_route.delete(path="/delete_game")
async def delete_game(game_id: uuid.UUID|str):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        res = new_db_source.delete("games", game_id)
        if res == []:
            raise HTTPException(status_code=404, detail="Нету такой игры")
        return JSONResponse(content=res, status_code=200)
    except:
        return JSONResponse(content={"error": "Ошибка при удалении игры"}, status_code=400)
    
@function_log
@games_route.put(path="/update_game")
async def update_game(new_game_data: Game_Update):
    """
        Обновление игры.
        Args:
            new_game_data (Game_Update): Данные игры для обновления.
        Returns:
            response (dict): Данные игры.
        Raises:
            HTTPException: Игра не найдена.
            InternalServerErrorException: Внутренняя ошибка сервера.
    """
    try:
        db_source = DBSource(settings.supabase.url, settings.supabase.key)
        db_source.connect()
        game_id = new_game_data.id
        new_game_data = new_game_data.model_dump()
        game = db_source.get_by_id("games", game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Игра не найдена")
        game = game[0]
        for i in new_game_data.keys():
            if new_game_data[i] == None:
                pass
            else:
                game[i] = new_game_data[i]
        game["id"] = str(game["id"])
        result = db_source.update("games", game, game_id)
        return JSONResponse(content=result[0], status_code=200)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as error:
        print(f"Ошибка при обновлении игры: {error}")
        return JSONResponse(
            content={"error": "Ошибка при обновлении игры"}, 
            status_code=400
        )


@function_log
@games_route.get(path="/view_game_with_params")
async def view_game_with_params(
    name: Optional[str] = Query(default=None),
    game_level: Optional[str] = Query(default=None),
    is_online: Optional[bool] = Query(default=None),
    place: Optional[str] = Query(default=None),
    number_of_players: Optional[int] = Query(default=None),
    seed: Optional[str] = Query(default=None)
):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        games = new_db_source.get_all("games")
        filtered_games = []
        for game in games:
            if name is not None and name.lower() not in game["name"].lower():
                continue
            if game_level is not None and game["game_level"].lower() != game_level.lower():
                continue
            if is_online is not None and game["is_online"] != is_online:
                continue
            if place is not None and game["place"].lower() != place.lower():
                continue
            if number_of_players is not None and game["number_of_players"] != number_of_players:
                continue
            if seed is not None and game["seed"] != seed:
                continue
            filtered_games.append(game)
        return JSONResponse(content=filtered_games, status_code=200)
    except:
        return JSONResponse(content={"error": "Ошибка при просмотре игры"}, status_code=400)
