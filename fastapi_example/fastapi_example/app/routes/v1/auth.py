from fastapi import APIRouter
from fastapi_example.modules.user.models import UserModel
from fastapi_example.adapters.supabase import get_supabase_client


route = APIRouter(prefix="/auth", tags=["auth"])


@route.post(path="/sign-up")
def sign_up(user: UserModel):
    try:
        supa = get_supabase_client()
        credentials = {
            "email": user.email,
            "password": user.password.get_secret_value(),
        }
        supa_user = supa.auth.sign_up(credentials=credentials)
        return supa_user
    except Exception as error:
        print(error)


@route.post(path="/sign-in")
def sign_in(user: UserModel):
    try:
        supa = get_supabase_client()
        credentials = {
            "email": user.email,
            "password": user.password.get_secret_value(),
        }
        supa_user = supa.auth.sign_in_with_password(credentials=credentials)
        return supa_user
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
