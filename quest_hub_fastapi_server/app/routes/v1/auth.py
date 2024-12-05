from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi import HTTPException
from model.user_model import User
from adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from model.character_list_model import CharacterList
from typing import Optional

route = APIRouter(prefix="/auth", tags=["auth"])


class SignUpUserModel(BaseModel):
    tg_id: str
    first_name: str
    role: str = "player"
    is_bot: bool = False
    username: Optional[str] = Field(default=None)
    age: int = None
    last_name: str = None
    is_premium: bool = False
    language_code: str = "rus"


@route.post(path="/sign-up")
def sign_up(sing_up_user_model: SignUpUserModel):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        new_user = User(
            tg_id=sing_up_user_model.tg_id,
            db_source=new_db_source,
            first_name=sing_up_user_model.first_name,
            username=sing_up_user_model.username,
            last_name=sing_up_user_model.last_name,
            role=sing_up_user_model.role,
            age=sing_up_user_model.age,
            is_bot=sing_up_user_model.is_bot,
            language_code=sing_up_user_model.language_code,
            is_premium=sing_up_user_model.is_premium,
        )
        user = new_user.insert()
        if user:
            return user
        else:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Service Unavailable",
                    "message": "Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору.",
                },
            )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": "Неизвестная ошибка на сервере. Обратитесь к администратору.",
            },
        )


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
