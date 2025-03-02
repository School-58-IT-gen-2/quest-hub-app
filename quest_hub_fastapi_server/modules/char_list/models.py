from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid

class Item(BaseModel):
    """Класс для работы с предметами."""
    id: Optional[str] = None
    count: Optional[int] = 1
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[int] = None
    cost: Optional[int] = None
    damage: Optional[str] = None
    damage_type: Optional[str] = None
    properties: Optional[List[str]] = None
    ac_base: Optional[int] = None
    dex_bonus: Optional[bool] = None
    max_dex_bonus: Optional[int] = None
    stealth_disadvantage: Optional[bool] = None # зарефакторить тут для апдейта

class Note(BaseModel):
    """Класс для работы с заметками."""
    title: Optional[str] = None
    text: Optional[str] = None
    id: Optional[str] = None # зарефакторить тут для апдейта

class CharListRequestModel(BaseModel):
    """Класс для работы с персонажами."""
    id: Optional[int] = None
    race: Optional[str] = None  # text
    character_class: Optional[str] = None  # text
    backstory: Optional[str] = None  # text
    notes: Optional[Note] = None  # json
    hp: Optional[int] = None  # int8
    initiative: Optional[int] = None  # int8
    lvl: Optional[int] = None  # int8
    passive_perception: Optional[int] = None  # int8
    speed: Optional[int] = None  # int8
    experience: Optional[int] = None  # int8
    ownership_bonus: Optional[int] = None  # int8
    ability_saving_throws: Optional[Dict[str,Any]] = None  # json
    death_saving_throws: Optional[int] = None  # int8
    interference: Optional[bool] = None  # bool
    advantages: Optional[bool] = None  # bool
    weapons_and_equipment: Optional[List[Item]] = None  # json
    spells: Optional[Dict[str, Any]] = None  # json
    traits_and_abilities: Optional[Dict[str, Any]] = None  # json
    languages: Optional[List[Any]] = None  # json
    special_features: Optional[Dict[str, Any]] = None  # json
    weaknesses: Optional[Dict[str, Any]] = None  # json
    npc_relations: Optional[Dict[str, Any]] = None  # json
    name: Optional[str] = None  # text
    gold: Optional[int] = None  # int8
    skills: Optional[List[Any]] = None  # json
    stat_modifiers: Optional[Dict[str, Any]] = None  # json
    stats: Optional[Dict[str, Any]] = None  # json
    user_id: Optional[str] = None  # text
    inspiration: Optional[bool] = True  # bool
    surname: Optional[str] = None # text
    inventory: Optional[List[Item]] = None # json
    age: Optional[int] = None # int8
    worldview: Optional[str] = None # text
    subrace: Optional[str] = None # text
    gender: Optional[str] = None # text


#Обработчик ошибок
class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Некорректный формат запроса"):
        super().__init__(status_code=400, detail=detail)


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: str = "Неизвестная ошибка на сервере. Обратитесь к администратору."):
        super().__init__(status_code=500, detail=detail)


class ServiceUnavailableException(HTTPException):
    def __init__(self, detail: str = "Запрашиваемый сервис или ресурс временно недоступен. Обратитесь к администратору."):
        super().__init__(status_code=503, detail=detail)