from quest_hub_fastapi_server.app.fastapi import app
from quest_hub_fastapi_server.app.routes import route


app.include_router(route)
