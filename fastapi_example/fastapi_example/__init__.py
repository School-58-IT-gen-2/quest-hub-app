import uvicorn

from fastapi_example.fastapi_example.modules.settings import settings


def start():
    uvicorn.run(
        app="fastapi_example.app:app",
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        reload=True,
    )
