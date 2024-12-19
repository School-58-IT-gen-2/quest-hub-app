from fastapi import FastAPI
from fastapi import Request, status


from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def lifespan(app: FastAPI):
    print("Server started")
    yield
    print("Server stopped")


# Инициализация приложения
app = FastAPI(lifespan=lifespan, title="QuestHub")


#Обработка исключений
@app.exception_handler(RequestValidationError)
async def handle_400_error(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request", 
                 "message": "Некорректный формат запроса"},
    )

@app.exception_handler(500)
def handle_500_error(request: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal Server Error", 
                 "message": "Неизвестная ошибка на сервере. Обратитесь к администратору."},
    )

@app.exception_handler(503)
def handle_503_error(request: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"error": "Service Unavailable", 
                 "message": "Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."},
    )
