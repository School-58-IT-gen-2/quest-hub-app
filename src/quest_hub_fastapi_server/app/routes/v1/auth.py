from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from model.user_model import User
from adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.app.schemas.auth import UserRequest, UserPutRequest

route = APIRouter(prefix="/auth", tags=["auth"])


@route.post(path="/user")
def create_user(
    body: UserRequest
):
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
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
    user = new_user.insert()
    return user

@route.get(path="/user")
def get_user(tg_id: int):
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    new_user = User(tg_id, new_db_source)
    new_user.insert()
    return new_user.__dict__()
    
@route.delete(path="/user")
def delete_user(tg_id: int):
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key) 
    new_db_source.connect()       
    new_user = User(tg_id, new_db_source)
    new_user.insert()
    return new_user.delete()

@route.put(path="/user")
def edit_user(
    body: UserPutRequest
    ):
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    new_user = User(body.tg_id, new_db_source)
    new_user.insert()
    return new_user.update({
                "first_name": body.first_name,
                "username": body.username,
                "age": body.age,
                "last_name": body.last_name,
                "is_premium": body.is_premium,
                "language_code": body.language_code
                })