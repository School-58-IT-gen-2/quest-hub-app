import uvicorn

from quest_hub_fastapi_server.modules.settings import settings

from logs.log import function_log

@function_log
def start():
    uvicorn.run(
        app="quest_hub_fastapi_server.app:app",
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        reload=True,
    )
