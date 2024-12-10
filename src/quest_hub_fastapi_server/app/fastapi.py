from fastapi import FastAPI


def lifespan(app: FastAPI):
    print("Server started")
    yield
    print("Server stopped")


# Инициализация приложения
app = FastAPI(lifespan=lifespan, title="QuestHub")
