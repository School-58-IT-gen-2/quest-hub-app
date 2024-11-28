from fastapi import APIRouter

from fastapi_example.app.routes.v1.auth import route as auth_route
from fastapi_example.app.routes.v1.user import route as user_route

route = APIRouter(prefix="/v1")

route.include_router(auth_route)
route.include_router(user_route)
