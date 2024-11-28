from fastapi import APIRouter
from fastapi_example.modules.user.models import UserModel


route = APIRouter(tags=["user"])


@route.get(
    path="/user",
    response_model=UserModel,
)
def get_user():
    try:
        user = UserModel(name="Сергей")
        return user
    except Exception as error:
        print(error)


@route.post(
    path="/user",
    response_model=UserModel,
)
def create_user(user: UserModel):
    try:
        return user
    except Exception as error:
        print(error)


@route.put(
    path="/user",
    response_model=UserModel,
)
def update_user(new_user: UserModel):
    try:
        exist_user = UserModel(name="Михаил")
        exist_user = new_user
        return exist_user
    except Exception as error:
        print(error)


@route.delete(
    path="/user",
    # response_model=UserModel,
)
def delete_user(user: UserModel):
    try:
        return {"status": "Ok"}
    except Exception as error:
        print(error)
