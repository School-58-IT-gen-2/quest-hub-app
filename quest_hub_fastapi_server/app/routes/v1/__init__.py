from fastapi import APIRouter

from quest_hub_fastapi_server.app.routes.v1.char_list import char_route
from quest_hub_fastapi_server.app.routes.v1.inventory import inventory_route
from quest_hub_fastapi_server.app.routes.v1.profile import profile_route
from quest_hub_fastapi_server.app.routes.v1.ammunition import ammunition_route
from quest_hub_fastapi_server.app.routes.v1.notes import note_route
from quest_hub_fastapi_server.app.routes.v1.char_info import char_info_route

route = APIRouter(prefix="/v1")

route.include_router(char_route)
route.include_router(char_info_route)
route.include_router(note_route)
route.include_router(ammunition_route)
route.include_router(inventory_route)
route.include_router(profile_route)
