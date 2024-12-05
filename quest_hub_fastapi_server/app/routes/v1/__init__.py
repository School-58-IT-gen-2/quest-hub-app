from fastapi import APIRouter
from quest_hub_fastapi_server.app.routes.v1.auth import route as auth_route
from quest_hub_fastapi_server.app.routes.v1.sync_async import route as sync_async_route
from quest_hub_fastapi_server.app.routes.v1.character_list_controller import (
    route as charlist_route,
)

route = APIRouter(prefix="/v1")

route.include_router(auth_route)
route.include_router(charlist_route)
route.include_router(sync_async_route)
