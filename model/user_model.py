from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from model.abstract_model import AbstractModel
from model.character_list_model import CharacterList
from typing import List, Optional, TYPE_CHECKING
import hashlib

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class User(AbstractModel):

    def __init__(self, username: str, tg_id: int, db_source: DBSource, first_name: str = None, last_name: str = None, role: str = None, id: int = None, age: int = None, is_bot: bool = None, language_code: str = None, is_premium: bool = None):
        """ 
        :param str username: Имя пользователя в Telegram
        :param int tg_id: id пользователя в Telegram
        :param DBSource db_source: Объект класса базы данных
        :param str first_name: Имя 
        :param str last_name: Фамилия
        :param str role: Роль (игрок или мастер)
        :param int id: id пользователя в supabase
        :param int age: Возраст
        :param bool is_bot: Является ли пользователь ботом ?????
        :param str language_code: ?????
        :param bool is_premium: ?????
        """
        self.__username = username
        self.__tg_id = tg_id
        self.__db_source = db_source
        self.__first_name = first_name
        self.__last_name = last_name
        self.__role = role
        self.__id = id
        self.__age = age
        self.__is_bot = is_bot
        self.__language_code = language_code
        self.__is_premium = is_premium

    @classmethod
    def get_by_login(cls, login: str, db_source: DBSource) -> Optional[User]:
        data = db_source.get_by_query(collection_name=cls._get_collection_name(), query={'login': login})
        if len(data) == 0:
            raise ValueError('No data was given')
        if len(data) > 1:
            raise ValueError('Too big data')
        return User(**data[0], db_source=db_source)
    
    def create_char_list(self,
                            character_name: str,
                            race: str,
                            character_class: str,
                            characteristics: dict,
                            hp: int,
                            alignment: str,
                            skills: dict,
                            weapons_and_equipment: dict,
                            saving_throws: dict,
                            death_saving_throws: int,
                            attacks: dict,
                            spells: dict,
                            passive_perception: int,
                            traits: list,
                            initiative: int,
                            level: int,
                            speed: int,
                            backstory: str,
                            experience: int,
                            valuables: dict,
                            diary: str,
                            notes: str,
                            languages: list,
                            npc_relations: dict):
        self.__char_list = CharacterList(self.__id, character_name, race, character_class, characteristics, hp, alignment, skills, weapons_and_equipment, saving_throws, death_saving_throws, attacks, spells, passive_perception, traits, initiative, level, speed, backstory, experience, valuables, diary, notes, languages, npc_relations)

    def get_char_list(self):
        return self.__char_list

    def __dict__(self) -> dict:
        return {"name": self.get_name(),
                "login": self.get_login(),
                "hash_password": self.get_password_hash(),
                'id': self.get_main_id()}
