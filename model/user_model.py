from model.abstract_model import AbstractModel
from model.character_list_model import CharacterList
from adapters.db_source import DBSource
from typing import List


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
        self.__char_lists = {}
        self.table_name = 'profiles'

    def insert(self):
        """Сохранение пользователя в базу данных"""
        data_list = self.get_by_value("tg_id", self.__tg_id)
        if len(data_list) == 0:
            insert_dict = self.__dict__()
            del insert_dict["id"]
            self.__id = self.__db_source.insert(self.table_name, insert_dict)[0]["id"]
        self.synchronize()
        return self.__dict__()
    
    def update(self, dict: dict) -> List[dict]:
        """
        Изменение данных о пользователе

        :param dict dict: Словарь новыми данными пользователя
        :return List[dict]: Список из словаря с новой строкой
        """
        if self.__id == None:
            raise Exception("id пользователя не может быть None. Добавьте пользователя в базу данных методом insert.")
        data_list = self.__db_source.update(self.table_name, dict, self.__id)
        self.synchronize()
        return data_list
    
    def delete(self) -> List[dict]:
        """Удаление пользователя из базы данных"""
        return self.__db_source.delete(self.table_name, self.__id)
    
    def get_by_id(self, id: str) -> List[dict]:
        """
        Получение пользователя по id

        :param str id: id пользователя
        :return List[dict]: Список из словаря со строкой таблицы
        """
        return self.__db_source.get_by_id(self.table_name, id)

    def get_by_value(self, parameter: str, parameter_value: any) -> List[dict]:
        """
        Получение пользователя по значению определенного параметра

        :param str parameter: Столбец, по которому происходит сравнение
        :param str / int / list parameter_value: Значение, по которому происходит сравнение
        :return List[dict]: Список из словаря со строкой таблицы
        """
        return self.__db_source.get_by_value(self.table_name, parameter, parameter_value)
    
    def synchronize(self):
        """Синхронизация объекта класса и данных в таблицах"""
        data_list = self.get_by_value("tg_id", self.__tg_id)
        if len(data_list) == 0:
            self.insert()
        else:
            data_dict = data_list[0]
            self.set_attributes(data_dict)
            for i in self.__db_source.get_by_value('character_list', "user_id", self.__id):
                char_list = CharacterList(self.__id, self.__db_source)
                char_list.synchronize(i["id"])
                self.__char_lists[char_list.id] = char_list

    
    def create_char_list(self,
                            name: str = None, race: str = None, character_class: str = None, stats: dict = None, hp: int = None, alignment: str = None, skills: dict = None, weapons_and_equipment: dict = None, ability_saving_throws: int = None, death_saving_throws: int = None, attacks: dict = None, spells: dict = None, passive_perception: int = None, traits_and_abilities: dict = None, initiative: int = None, lvl: int = None, speed: int = None, backstory: str = None, experience: int = None, valuables: dict = None, diary: str = None, notes: str = None, languages: dict = None, npc_relations: dict = None, inspiration: int = None, interference: bool = None, ownership_bonus: int = None, advantages: bool = None, attribute_points: int = None, special_fours: dict = None, weaknesses: dict = None, damage: dict = None, stat_modifiers: dict = None) -> CharacterList:
        """Создание листа персонажа пользователя"""
        if self.__id == None:
            raise Exception("id пользователя не может быть None. Добавьте пользователя в базу данных методом insert.")
        char_list = CharacterList(self.__id, self.__db_source, None,  name, race, character_class, stats, hp, alignment, skills, weapons_and_equipment, ability_saving_throws, death_saving_throws, attacks, spells, passive_perception, traits_and_abilities, initiative, lvl, speed, backstory, experience, valuables, diary, notes, languages, npc_relations, inspiration, interference, ownership_bonus, advantages, attribute_points, special_fours, weaknesses, damage, stat_modifiers)
        char_list.insert()
        self.__char_lists[char_list.id] = char_list

    def get_char_lists(self) -> dict:
        """Получение листа персонажа пользователя"""
        return self.__char_lists

    def __dict__(self) -> dict:
        """Вывод всех параметров пользователя в формате словаря"""
        return {
            "id": self.__id,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "role": self.__role,
            "is_bot": self.__is_bot,
            "language_code": self.__language_code,
            "is_premium": self.__is_premium,
            "username": self.__username,
            "age": self.__age,
            "tg_id": self.__tg_id
        }
    
    def set_attributes(self, attr_dict: dict):
        """
        Установка параметров пользователя, заданных в словаре

        :param dict attr_dict: Словарь с параметрами, которые нужно установить пользователю
        """
        for key in attr_dict:
            setattr(self, '_' + self.__class__.__name__ + '__' + key, attr_dict[key])
