from fastapi import APIRouter
from fastapi import HTTPException
from model.user_model import User
from adapters.db_source import DBSource
from net_config import settings


route = APIRouter(prefix="/auth", tags=["auth"])

@route.post(path="/sign-up")
def sign_up(
            first_name: str,
            last_name: str,
            role: str,
            is_bot: bool,
            language_code: str,
            is_premium: bool,
            username: str,
            age: int,
            tg_id: int,
        ):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key) 
        new_db_source.connect()
        new_user = User(
            tg_id, new_db_source, first_name, username, last_name, role, 
            age=age, is_bot=is_bot, language_code=language_code, is_premium=is_premium
            )
        user = new_user.insert()
        if user:
            return user
        else: 
            raise HTTPException(status_code=503, detail="Database unreachable")
    except Exception as error:
        print(error)


@route.get(path="/sign-in")
def sign_in(tg_id: int, first_name: str):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)        
        new_user = User(tg_id, new_db_source, first_name)
        new_user.insert()
        return new_user
    except Exception as error:
        print(error)


@route.post(path="/sign-out")
def sign_out():
    try:
        return {"status": "Ok"}
    except Exception as error:
        print(error)
