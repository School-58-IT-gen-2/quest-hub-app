from fastapi import APIRouter
from fastapi import HTTPException
from model.user_model import User
from adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.app.schemas.auth import UserRequest, UserPutRequest

route = APIRouter(prefix="/auth", tags=["auth"])


@route.post(path="/user")
def create_user(
    body: UserRequest
):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        try:
            new_user = User(
                body.tg_id,
                new_db_source,
                body.first_name,
                body.username,
                body.last_name,
                body.role,
                age=body.age,
                is_bot=body.is_bot,
                language_code=body.language_code,
                is_premium=body.is_premium,
            )
        except:
            raise HTTPException(status_code=400, 
                                detail={"error": "Invalid request", 
    "message":"Некорректный формат запроса"})
        user = new_user.insert()
        if user:
            return user.__dict__()
        else: 
            raise HTTPException(status_code=503, 
                                detail={"error": "Service Unavailable", 
    "message":"Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."})
    except HTTPException as exception:
        if exception.status_code in [400, 503]:
            raise exception
        raise HTTPException(status_code=500, 
    detail={"error": "Internal Server Error", 
            "message":"Неизвестная ошибка на сервере. Обратитесь к администратору."})

@route.get(path="/user")
def get_user(tg_id: int):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        try:
            new_user = User(tg_id, new_db_source)
            new_user.insert()
        except:
            raise HTTPException(status_code=400, 
                                detail={"error": "Invalid request", 
    "message":"Некорректный формат запроса"})
        if new_user:
            return new_user.__dict__()
        else: 
            raise HTTPException(status_code=503, 
                                detail={"error": "Service Unavailable", 
    "message":"Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."})
    except HTTPException as exception:
        if exception.status_code in [400, 503]:
            raise exception
        raise HTTPException(status_code=500, 
    detail={"error": "Internal Server Error", 
            "message":"Неизвестная ошибка на сервере. Обратитесь к администратору."})
    
@route.delete(path="/user")
def delete_user(tg_id: int):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key) 
        new_db_source.connect()       
        try:
            new_user = User(tg_id, new_db_source)
            new_user.insert()
        except:
            raise HTTPException(status_code=400, 
                                detail={"error": "Invalid request", 
    "message":"Некорректный формат запроса"})
        if new_user:
            return new_user.delete()
        else: 
            raise HTTPException(status_code=503, 
                                detail={"error": "Service Unavailable", 
    "message":"Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."})
    except HTTPException as exception:
        if exception.status_code in [400, 503]:
            raise exception
        raise HTTPException(status_code=500, 
    detail={"error": "Internal Server Error", 
            "message":"Неизвестная ошибка на сервере. Обратитесь к администратору."})
    
@route.put(path="/user")
def edit_user(
    body: UserPutRequest
    ):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        try:
            new_user = User(body.tg_id, new_db_source)
            new_user.insert()
        except:
            raise HTTPException(status_code=400, 
                                detail={"error": "Invalid request", 
                                            "message":"Некорректный формат запроса"})
        if new_user:
            return new_user.update({
                        "first_name": body.first_name,
                        "username": body.username,
                        "age": body.age,
                        "last_name": body.last_name,
                        "is_premium": body.is_premium,
                        "language_code": body.language_code
                        })
        else: 
            raise HTTPException(status_code=503, 
                                detail={"error": "Service Unavailable", 
    "message":"Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."})
    except HTTPException as exception:
        if exception.status_code in [400, 503]:
            raise exception
        raise HTTPException(status_code=500, 
    detail={"error": "Internal Server Error", 
            "message":"Неизвестная ошибка на сервере. Обратитесь к администратору."})