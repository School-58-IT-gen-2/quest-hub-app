import requests
import json
import uuid
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
    Note,Item,Spell,
    BadRequestException,
    InternalServerErrorException,
    ServiceUnavailableException
)

to_ai = APIRouter(prefix="/ai",tags=["ai"])


def ask_llama(question, model="llama3.2", temperature=1):
    url = "http://localhost:11345/api/generate"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "model": model,
        "prompt": question,
        "temperature": temperature,
        "stream": False
    }
    
    try:
        # Проверка доступности сервера
        health_check = requests.get("http://localhost:11345/")
        health_check.raise_for_status()
        
        # Основной запрос с диагностикой
        response = requests.post(
            url,
            data=json.dumps(payload),  # Явная сериализация JSON
            headers=headers,
            timeout=120
        )
        
        response.raise_for_status()
        return response.json().get('response', 'No response in JSON')
    
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

class Prompt(BaseModel):
    question: str

class Char(BaseModel):
    char: dict

@to_ai.post("/ask_llama")
async def ask_lama(prompt:Prompt, char:Char):
    res = prompt.question + str(json.dumps(char.char,ensure_ascii=False))
    print(res)
    response = ask_llama(res)
    return JSONResponse(content=response, status_code=200)


# @to_ai.post("/ask_gpt")
# async def ask_gpt(prompt:Prompt, char:Char):
#     res = prompt.question + str(json.dumps(char.char,ensure_ascii=False))
#     print(res)
#     response = ask_llama(res)
#     return JSONResponse(content=response, status_code=200)