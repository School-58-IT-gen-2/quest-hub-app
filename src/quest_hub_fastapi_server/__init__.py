import uvicorn

from quest_hub_fastapi_server.modules.settings import settings


def start():
    uvicorn.run(
        app="quest_hub_fastapi_server.app:app",
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        reload=True,
    )
