from fastapi import APIRouter
from fastapi_example.modules.user.models import UserModel
from fastapi_example.adapters.supabase import get_supabase_client
from ......model.user_model import User
from ......adapters.db_source import DBSource
from ......net_config import settings


route = APIRouter(prefix="/auth", tags=["auth"])


@route.post(path="/sign-up")
def sign_up(tg_id: int, first_name: str):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)        
        new_user = User(tg_id, new_db_source, first_name)
        new_user.insert()
        return new_user.__dict__()
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
def sign_out(user: UserModel):
    try:
        supa = get_supabase_client()
        credentials = {
            "email": user.email,
            "password": user.password.get_secret_value(),
        }
        return supa.auth.sign_out()
    except Exception as error:
        print(error)
