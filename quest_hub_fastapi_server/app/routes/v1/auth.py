from fastapi import APIRouter
from fastapi import HTTPException
from model.user_model import User
from adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings


route = APIRouter(prefix="/auth", tags=["auth"])

@route.post(path="/user")
def create_user(
    tg_id: int,
    first_name: str = "",
    role: str = "player",
    is_bot: bool = False,
    username: str = None,
    age: int = None,
    last_name: str = None,
    is_premium: bool = False,
    language_code: str = "rus",
):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        new_user = User(
            tg_id,
            new_db_source,
            first_name,
            username,
            last_name,
            role,
            age=age,
            is_bot=is_bot,
            language_code=language_code,
            is_premium=is_premium,
        )
        user = new_user.insert()
        if user:
            return user
        else: 
            raise HTTPException(status_code=503, 
                                detail={"error": "Service Unavailable", 
    "message":"Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."})
    except:
        raise HTTPException(status_code=500, 
    detail={"error": "Internal Server Error", 
            "message":"Неизвестная ошибка на сервере. Обратитесь к администратору."})

@route.get(path="/user?tg_id={tg_id}")
def get_user(tg_id: int):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_user = User(tg_id, new_db_source)
        new_user.insert()
        if new_user:
            return new_user
        else: 
            raise HTTPException(status_code=503, 
                                detail={"error": "Service Unavailable", 
    "message":"Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."})
    except:
        raise HTTPException(status_code=500, 
    detail={"error": "Internal Server Error", 
            "message":"Неизвестная ошибка на сервере. Обратитесь к администратору."})
    
@route.delete(path="/user?id={tg_id}")
def delete_user(tg_id: int):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)        
        new_user = User(tg_id, new_db_source)
        new_user.insert()
        if new_user:
            return new_user.delete()
        else: 
            raise HTTPException(status_code=503, 
                                detail={"error": "Service Unavailable", 
    "message":"Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."})
    except:
        raise HTTPException(status_code=500, 
    detail={"error": "Internal Server Error", 
            "message":"Неизвестная ошибка на сервере. Обратитесь к администратору."})
    
@route.put(path="/user")
def edit_user(
    tg_id: int,
    first_name: str = "",
    username: str = None,
    age: int = None,
    last_name: str = None,
    is_premium: bool = False,
    language_code: str = "rus",
    ):
    if True:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_user = User(tg_id, new_db_source)
        new_user.insert()
        if new_user:
            return new_user.update({
                        "first_name": first_name,
                        "username": username,
                        "age": age,
                        "last_name": last_name,
                        "is_premium": is_premium,
                        "language_code": language_code
                        })
        else: 
            raise HTTPException(status_code=503, 
                                detail={"error": "Service Unavailable", 
    "message":"Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."})