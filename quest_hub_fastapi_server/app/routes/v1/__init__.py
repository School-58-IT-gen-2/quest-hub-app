from fastapi import APIRouter

from quest_hub_fastapi_server.app.routes.v1.auth import route as auth_route

route = APIRouter(prefix="/v1")

route.include_router(auth_route)

