from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class RequestProfileModel(BaseModel):
    tg_id: int
    first_name: str
    role: str = "player"
    is_bot: bool
    username: Optional[str] = None
    age: Optional[int] = None
    last_name: Optional[str] = None
    is_premium: Optional[bool] = None
    language_code: str


class ResponseProfileModel(BaseModel):
    id: UUID
    tg_id: int
    first_name: str
    role: str = "player"
    is_bot: bool
    username: Optional[str] = None
    age: Optional[int] = None
    last_name: Optional[str] = None
    is_premium: Optional[bool] = None
    language_code: str


class ProfileUpdateModel(BaseModel):
    tg_id: int
    first_name: str
    username: Optional[str] = None
    age: Optional[int] = None
    last_name: Optional[str] = None
    is_premium: Optional[bool] = None
    language_code: str
