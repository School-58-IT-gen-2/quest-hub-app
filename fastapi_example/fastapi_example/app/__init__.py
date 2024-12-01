from fastapi_example.app.fastapi import app
from fastapi_example.app.routes import route


app.include_router(route)
