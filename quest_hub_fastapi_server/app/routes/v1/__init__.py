from fastapi import APIRouter

from quest_hub_fastapi_server.app.routes.v1.char_list import char_route
from quest_hub_fastapi_server.app.routes.v1.inventory import inventory_route
from quest_hub_fastapi_server.app.routes.v1.profile import profile_route
from quest_hub_fastapi_server.app.routes.v1.ammunition import ammunition_route
from quest_hub_fastapi_server.app.routes.v1.notes import note_route
from quest_hub_fastapi_server.app.routes.v1.char_info import char_info_route
from quest_hub_fastapi_server.app.routes.v1.spells import spell_route
from quest_hub_fastapi_server.app.routes.v1.traits_and_abilities import traits_and_abilities_route
from quest_hub_fastapi_server.app.routes.v1.to_ai import to_ai
from quest_hub_fastapi_server.app.routes.v1.games import games_route

route = APIRouter(prefix="/v1")

route.include_router(char_route)
route.include_router(char_info_route)
route.include_router(note_route)
route.include_router(ammunition_route)
route.include_router(inventory_route)
route.include_router(spell_route)
route.include_router(traits_and_abilities_route)
route.include_router(to_ai)
route.include_router(profile_route)
route.include_router(games_route)
