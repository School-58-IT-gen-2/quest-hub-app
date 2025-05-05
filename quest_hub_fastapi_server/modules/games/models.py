from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid
import datetime
from enum import Enum

class Game_Level(Enum):
    """
    Перечисление уровней игры.
    """
    any = None
    easy = "Легкий"
    medium = "Средний"
    hard = "Сложный"
    social = "Социальный"

class Game(BaseModel):
    """
    Модель игры.
    """
    id: Optional[uuid.UUID] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    format: str
    city: str
    level: Optional[Game_Level] = None
    player_count: int
    master_id: str
    players_id: Optional[List[str]] = None
    seed: Optional[str] = None


class Game_Update(BaseModel):
    """
    Модель для обновления игры.
    """
    id: Optional[uuid.UUID] = None 
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    is_online: Optional[bool] = None
    place: Optional[str] = None
    game_level: Optional[Game_Level] = None
    number_of_players: Optional[int] = None
    master_id: Optional[str] = None
    players_id: Optional[List[str]] = None
    seed: Optional[str] = None
