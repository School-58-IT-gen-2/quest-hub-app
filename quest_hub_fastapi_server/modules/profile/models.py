from pydantic import BaseModel
from typing import Optional


class ProfileRequest(BaseModel):
    """Класс для работы с профилем пользователя. (общий вид)"""
    tg_id: int
    first_name: str
    role: str = "player"
    is_bot: bool
    username: Optional[str] = None
    age: Optional[int] = None
    last_name: Optional[str] = None
    is_premium: Optional[bool] = None
    language_code: str


class ProfilePutRequest(BaseModel):
    """Класс для работы с профилем пользователя. (только для обновления данных)"""
    tg_id: int
    first_name: str
    username: Optional[str] = None
    age: Optional[int] = None
    last_name: Optional[str] = None
    is_premium: Optional[bool] = None
    language_code: str
