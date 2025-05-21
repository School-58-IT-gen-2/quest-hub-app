import uuid
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.games.models import *
from logs.log import function_log

help_route = APIRouter(prefix="/help", tags=["help"])

class Help(BaseModel):
    question: str
    category: str

@function_log
@help_route.post(path="/save_question")
async def get_help(help_data: Help):
    """
        Сохраняет вопрос в базе данных.
        Args:
            help_data (Help): вопрос.
        Returns:
            response (dict): сохраненный вопрос.
    """
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        help_data = help_data.model_dump()
        result = new_db_source.insert("questions", help_data)
        if result != []:
            return JSONResponse(content=result[0],status_code=201)
        else:
            return JSONResponse(content={"error": "Ошибка в вопросах"}, status_code=500)
    except Exception as error:
        return JSONResponse(content={"error": "Ошибка в вопросах"}, status_code=400)