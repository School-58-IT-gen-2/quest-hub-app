# import requests
# import json
# import uuid
# import g4f
# from g4f import Client
# from pydantic import BaseModel
# from fastapi import APIRouter, HTTPException
# from fastapi.responses import JSONResponse
# from typing import Optional
# from quest_hub_fastapi_server.adapters.db_source import DBSource
# from quest_hub_fastapi_server.modules.settings import settings
# from quest_hub_fastapi_server.modules.char_list.models import (
#     CharListRequestModel,
#     Note,Item,Spell,
#     BadRequestException,
#     InternalServerErrorException,
#     ServiceUnavailableException
# )

# from logs.log import function_log

# to_ai = APIRouter(prefix="/ai",tags=["ai"])


# # def ask_llama(question, model="llama3.2", temperature=1):
# #     url = "http://localhost:11345/api/generate"
# #     headers = {'Content-Type': 'application/json'}
# #     payload = {
# #         "model": model,
# #         "prompt": question,
# #         "temperature": temperature,
# #         "stream": False
# #     }
    
# #     try:
# #         # Проверка доступности сервера
# #         health_check = requests.get("http://localhost:11345/")
# #         health_check.raise_for_status()
        
# #         # Основной запрос с диагностикой
# #         response = requests.post(
# #             url,
# #             data=json.dumps(payload),  # Явная сериализация JSON
# #             headers=headers,
# #             timeout=120
# #         )
        
# #         response.raise_for_status()
# #         return response.json().get('response', 'No response in JSON')
    
# #     except requests.exceptions.HTTPError as e:
# #         return f"HTTP Error {e.response.status_code}: {e.response.text}"
# #     except Exception as e:
# #         return f"Error: {str(e)}"

# def ask_g4f(question, model="gpt-3.5-turbo"):
#     response = g4f.ChatCompletion.create(
#         model=g4f.models.gpt_4,
#         messages=[{"role": "user", "content": question}],
#     )
#     return response

# def claude(question, model="gpt-3.5-turbo"):
#     response = g4f.ChatCompletion.create(
#         model=g4f.models.claude_3_7_sonnet,
#         messages=[{"role": "user", "content": question}],
#     )
#     return response

# def deepseek(question, model="gpt-3.5-turbo"):
#     response = g4f.ChatCompletion.create(
#         model=g4f.models.deepseek_v3,
#         messages=[{"role": "user", "content": question}],
#     )
#     return response

# class Prompt(BaseModel):
#     question: str

# class Char(BaseModel):
#     char: dict

# # @to_ai.post("/ask_llama")
# # async def ask_lama(prompt:Prompt, char:Char):
# #     res = prompt.question + str(json.dumps(char.char,ensure_ascii=False))
# #     response = ask_llama(res)
# #     return JSONResponse(content=response, status_code=200)

# @function_log
# @to_ai.post("/ask_gpt")
# async def ask_gpt(prompt: Prompt, char: Char):
#     res = prompt.question + str(json.dumps(char.char, ensure_ascii=False))
#     response = ask_g4f(res)
#     return JSONResponse(content=response, status_code=200)

# @function_log
# @to_ai.post("/ask_claude")
# async def ask_gemini(prompt: Prompt, char: Char):
#     res = prompt.question + str(json.dumps(char.char, ensure_ascii=False))
#     response = claude(res)
#     return JSONResponse(content=response,status_code=200)

# @function_log
# @to_ai.post("/ask_deepseek")
# async def ask_gemini(prompt: Prompt, char: Char):
#     res = prompt.question + str(json.dumps(char.char, ensure_ascii=False))
#     response = deepseek(res)
#     return JSONResponse(content=response,status_code=200)