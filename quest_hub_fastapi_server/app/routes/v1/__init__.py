from fastapi import APIRouter

from quest_hub_fastapi_server.app.routes.v1.char_list import char_route
from quest_hub_fastapi_server.app.routes.v1.profile import profile_route

route = APIRouter(prefix="/v1")

route.include_router(char_route)
route.include_router(profile_route)
