from pydantic import BaseModel


class UserRequest(BaseModel):
    tg_id: int
    first_name: str = ""
    role: str = "player"
    is_bot: bool = False
    username: str = None
    age: int = None
    last_name: str = None
    is_premium: bool = False
    language_code: str = "rus"

class UserPutRequest(BaseModel):
    tg_id: int
    first_name: str = ""
    username: str = None
    age: int = None
    last_name: str = None
    is_premium: bool = False
    language_code: str = "rus"
