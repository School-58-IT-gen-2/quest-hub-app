import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.games.models import *

games_route = APIRouter(prefix="/games", tags=["games"])


@games_route.post(path="/create")
async def create_game(game_data: Game):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        game = game_data.model_dump()
        game.pop("id")
        game.pop("created_at")
        #game["game_level"] = game["game_level"].value
        game["players_id"] = [str(i) for i in  game["players_id"]]
        game["master_id"] = str(game["master_id"])
        game["game_level"] = str(game["game_level"].value)
        print(game)
        result = new_db_source.insert("games", game)
        if result != []:
            return JSONResponse(content=result[0],status_code=201)
        else:
            return JSONResponse(content={"error": "Ошибка при создании игры"}, status_code=500)
    except Exception as error:
        return JSONResponse(content={"error": "Ошибка при создании игры"}, status_code=500)
    
#put, get/get all, delete

@games_route.get(path="/view_game")
async def view_part_game(game_id: Optional[uuid.UUID|str] = None):
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
        return JSONResponse(content={"error": "Ошибка при просмотре игры"}, status_code=500)
    
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
        return JSONResponse(content={"error": "Ошибка при удалении игры"}, status_code=500)
    
@games_route.put(path="/update_game")
async def update_game(game_id: uuid.UUID|str, new_game_data: Game):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        game = new_game_data.model_dump()
        game.pop("id")
        game.pop("created_at")
        #game["game_level"] = game["game_level"].value
        game["players_id"] = [str(i) for i in  game["players_id"]]
        game["master_id"] = str(game["master_id"])
        game["game_level"] = str(game["game_level"].value)
        res = new_db_source.update("games", game, game_id)
        if res == []:
            raise HTTPException(status_code=404, detail="Нету такой игры")
        return JSONResponse(content=res, status_code=200)
    except:
        return JSONResponse(content={"error": "Ошибка при обновлении игры"}, status_code=500)