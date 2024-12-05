import uvicorn

from fastapi import FastAPI



async def lifespan(app: FastAPI):
    print("Server started")
    yield
    print("Server stopped")


app = FastAPI(lifespan=lifespan)
