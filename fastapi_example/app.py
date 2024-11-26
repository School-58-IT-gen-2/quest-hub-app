import uvicorn

from fastapi import FastAPI

from fastapi_example.model.item import Item
from fastapi_example.model.user import User


async def lifespan(app: FastAPI):
    print("Server started")
    yield
    print("Server stopped")


app = FastAPI(lifespan=lifespan)


@app.get("/user")
def get_user():
    return {"name": "Сергей"}


@app.post("/user/{user_name}/{user_id}")
def create_user(user_name: str = "NONE", user_id: str = "123123"):
    try:
        # типо сохраняем в БД
        response = {"message": "created"}
        user = User()
        print(user_id)
        user.print_name()
        return response
    except Exception as e:
        print("Error: ", e)
        return {"message": "User creation failed"}

@app.post("/char")
def create_character(name: str = 0, level: int = 1, char_class: str = "bard"):

    response = {"name": name, "level": level, "char_class": char_class}

    return response

@app.post("/item")
def create_item(item: Item):
    new_item = item
    item.price += 1

    return new_item

@app.put("/data")
def put_data(data: User):
    return {"result": "Updated"}

@app.get("/data")
def get_data():
    return {"data": "ACCESS DENIED"}
