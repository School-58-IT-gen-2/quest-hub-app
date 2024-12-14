from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from quest_hub_fastapi_server.adapters.db_source import DBSource


def lifespan(app: FastAPI):
    db_source = DBSource()
    print("Server started")
    yield
    print("Server stopped")


# Инициализация приложения
app = FastAPI(lifespan=lifespan, title="QuestHub")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "FastAPI server", "message": exc.detail},
    )
