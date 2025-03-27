from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid
import datetime
from enum import Enum

class Game_Level(Enum):
    """
    Перечисление уровней игры.
    """
    easy = "легко"
    medium = "средне"
    hard = "сложно"
    very_hard = "пипец сложно"

class Game(BaseModel):
    """
    Модель игры.
    """
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    created_at: datetime.datetime
    is_online: bool
    place: str
    game_level: Optional[Game_Level] = None
    number_of_players: int
    master_id: uuid.UUID
    players_id: Optional[List[uuid.UUID]] = None
    seed: Optional[str] = None
