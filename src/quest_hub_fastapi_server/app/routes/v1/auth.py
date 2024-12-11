from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
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
def sign_up(
    tg_id: int,
    first_name: str,
    role: str = "player",
    is_bot: bool = False,
    username: str = None,
    age: int = None,
    last_name: str = None,
    is_premium: bool = False,
    language_code: str = "rus"):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        new_user = User(
            tg_id=tg_id,
            db_source=new_db_source,
            first_name=first_name,
            username=username,
            last_name=last_name,
            role=role,
            age=age,
            is_bot=is_bot,
            language_code=language_code,
            is_premium=is_premium,
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
        new_db_source.connect()
        new_user = User(tg_id, new_db_source, first_name)
        new_user.insert()
        return new_user.__dict__()
    except Exception as error:
        print(error)


@route.post(path="/sign-out")
def sign_out():
    try:
        return {"status": "Ok"}
    except Exception as error:
        print(error)

@route.get(path="/git_actions_test")
def test_git_actions():
    return "Git Actions work"