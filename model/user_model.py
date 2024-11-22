from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from model.abstract_model import AbstractModel
from model.character_list_model import CharacterList
from typing import List, Optional, TYPE_CHECKING
import hashlib

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class User(AbstractModel):

    def __init__(self, tg_id: int, db_source: DBSource, first_name: str, username: str = None, last_name: str = None, role: str = None, id: str = None, age: int = None, is_bot: bool = None, language_code: str = None, is_premium: bool = None):
        """ 
        :param int tg_id: id пользователя в Telegram
        :param DBSource db_source: Объект класса базы данных
        :param str first_name: Имя 
        :param str username: Имя пользователя в Telegram
        :param str last_name: Фамилия
        :param str role: Роль (игрок или мастер)
        :param str id: id пользователя в supabase
        :param int age: Возраст
        :param bool is_bot: Является ли пользователь ботом
        :param str language_code: Язык системы пользователя
        :param bool is_premium: Есть ли Telegram Premium
        """
        self.__tg_id = tg_id
        self.__db_source = db_source
        self.__first_name = first_name
        self.__username = username
        self.__last_name = last_name
        self.__role = role
        self.__id = id
        self.__age = age
        self.__is_bot = is_bot
        self.__language_code = language_code
        self.__is_premium = is_premium
        self.__char_list = None

    def save(self):
        """Сохранение пользователя в базу данных"""
        if self.__dict__()["id"] != None:
            insert_dict = self.__dict__()
            del insert_dict["id"]
            self.__db_source.insert('profiles', insert_dict)
            self.__id = dict(self.__db_source.get_by_value('profiles', "tg_id", self.__tg_id))["data"][0]["id"]
    
    def create_char_list(self,
                            name: str = None, race: str = None, character_class: str = None, stats: dict = None, hp: int = None, alignment: str = None, skills: dict = None, weapons_and_equipment: dict = None, ability_saving_throws: int = None, death_saving_throws: int = None, attacks: dict = None, spells: dict = None, passive_perception: int = None, traits_and_abilities: dict = None, initiative: int = None, lvl: int = None, speed: int = None, backstory: str = None, experience: int = None, valuables: dict = None, diary: str = None, notes: str = None, languages: dict = None, npc_relations: dict = None, inspiration: int = None, interference: bool = None, ownership_bonus: int = None, advantages: bool = None, attribute_points: int = None, special_fours: dict = None, weaknesses: dict = None, damage: dict = None, stat_modifiers: dict = None):
        if self.__id == None:
            raise Exception("id пользователя не может быть None. Добавьте пользователя в базу данных методом save перед созданием его листа персонажа.")
        self.__char_list = CharacterList(self.__id, name, race, character_class, stats, hp, alignment, skills, weapons_and_equipment, ability_saving_throws, death_saving_throws, attacks, spells, passive_perception, traits_and_abilities, initiative, lvl, speed, backstory, experience, valuables, diary, notes, languages, npc_relations, inspiration, interference, ownership_bonus, advantages, attribute_points, special_fours, weaknesses, damage, stat_modifiers)

    def get_char_list(self):
        return self.__char_list

    def __dict__(self) -> dict:
        return {
            "id": self.__id,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "role": self.__role,
            "char_list": self.__char_list,
            "is_bot": self.__is_bot,
            "language_code": self.__language_code,
            "is_premium": self.__is_premium,
            "username": self.__username,
            "age": self.__age,
            "tg_id": self.__tg_id
        }
