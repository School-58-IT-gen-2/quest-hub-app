from fastapi import APIRouter

from fastapi_example.app.routes.v1 import route as v1_route

route = APIRouter(prefix="/api")

route.include_router(v1_route)
