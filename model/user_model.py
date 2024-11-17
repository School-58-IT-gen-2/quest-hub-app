from __future__ import annotations  # нужно чтобы parse мог быть типизирован

from model.abstract_model import AbstractModel
from character_list_model import CharacterList
from typing import List, Optional, TYPE_CHECKING
import hashlib

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class User(AbstractModel):

    def __init__(self, name: str, login: str, hash_password: Optional[str] = None,
                 password: Optional[str] = None, id: int = None):
        """
            :param login: Логин
            :param password_hash: Пароль
            :param name: Имя пользователя
        """
        self.__login = login
        if hash_password is None and password is not None:
            self.__password_hash = hashlib.sha256(password.encode()).hexdigest()
        elif password is None and hash_password is not None:
            self.__password_hash = hash_password
        else:
            raise ValueError('Ошибка создания: должен присутствовать password ИЛИ hash_password')
        self.__name = name
        self.__id = id

    @classmethod
    def get_by_login(cls, login: str, db_source: DBSource) -> Optional[User]:
        data = db_source.get_by_query(collection_name=cls._get_collection_name(), query={'login': login})
        if len(data) == 0:
            raise ValueError('No data was given')
        if len(data) > 1:
            raise ValueError('Too big data')
        return User(**data[0], db_source=db_source)
    
    def create_character_list(self,
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
        self.character_list = CharacterList(self.__id, character_name, race, character_class, characteristics, hp, alignment, skills, weapons_and_equipment, saving_throws, death_saving_throws, attacks, spells, passive_perception, traits, initiative, level, speed, backstory, experience, valuables, diary, notes, languages, npc_relations)

    def get_login(self) -> str:
        return self.__login

    def get_password_hash(self) -> str:
        return self.__password_hash

    def get_name(self) -> str:
        return self.__name

    def get_main_id(self) -> int:
        return self.__id

    def __str__(self):
        return f"Пользователь {self.get_name()} с логином {self.get_login()}"

    def __dict__(self) -> dict:
        return {"name": self.get_name(),
                "login": self.get_login(),
                "hash_password": self.get_password_hash(),
                'id': self.get_main_id()}

    def compare_hash(self, password: str) -> bool:
        return self.__password_hash == hashlib.sha256(password.encode()).hexdigest()