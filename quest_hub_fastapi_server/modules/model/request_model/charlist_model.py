from pydantic import BaseModel
from typing import Optional, Dict, Any


class CharListRequestModel(BaseModel):
    race: Optional[str] = None  # text
    character_class: Optional[str] = None  # text
    backstory: Optional[str] = None  # text
    notes: Optional[str] = None  # text
    diary: Optional[str] = None  # text
    hp: Optional[int] = None  # int8
    initiative: Optional[int] = None  # int8
    lvl: Optional[int] = None  # int8
    passive_perception: Optional[int] = None  # int8
    speed: Optional[int] = None  # int8
    experience: Optional[int] = None  # int8
    ownership_bonus: Optional[int] = None  # int8
    ability_saving_throws: Optional[int] = None  # int8
    death_saving_throws: Optional[int] = None  # int8
    interference: Optional[bool] = None  # bool
    advantages: Optional[bool] = None  # bool
    weapons_and_equipment: Optional[Dict[str, Any]] = None  # json
    spells: Optional[Dict[str, Any]] = None  # json
    traits_and_abilities: Optional[Dict[str, Any]] = None  # json
    languages: Optional[Dict[str, Any]] = None  # json
    attacks: Optional[Dict[str, Any]] = None  # json
    special_features: Optional[Dict[str, Any]] = None  # json
    weaknesses: Optional[Dict[str, Any]] = None  # json
    damage: Optional[Dict[str, Any]] = None  # json
    npc_relations: Optional[Dict[str, Any]] = None  # json
    name: Optional[str] = None  # text
    valuables: Optional[Dict[str, Any]] = None  # json
    skills: Optional[Dict[str, Any]] = None  # json
    stat_modifiers: Optional[Dict[str, Any]] = None  # json
    stats: Optional[Dict[str, Any]] = None  # json
    user_id: Optional[str] = None  # text
    inspiration: bool = True  # bool