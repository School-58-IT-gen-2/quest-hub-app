from typing import List

from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.abstract_model import AbstractModel

from logs.log import function_log


class CharacterList(AbstractModel):
    """Класс листа персонажа."""

    @function_log
    def __init__(
        self,
        user_id: str,
        db_source: DBSource,
        id: int = None,
        name: str = None,
        race: str = None,
        character_class: str = None,
        stats: dict = None,
        hp: int = None,
        alignment: str = None,
        skills: dict = None,
        weapons_and_equipment: dict = None,
        ability_saving_throws: dict = None,
        death_saving_throws: dict = None,
        attacks: dict = None,
        spells: dict = None,
        passive_perception: int = None,
        traits_and_abilities: dict = None,
        initiative: int = None,
        lvl: int = None,
        speed: int = None,
        backstory: str = None,
        experience: int = None,
        valuables: dict = None,
        diary: str = None,
        notes: str = None,
        languages: dict = None,
        npc_relations: dict = None,
        inspiration: bool = None,
        interference: bool = None,
        ownership_bonus: int = None,
        advantages: bool = None,
        attribute_points: int = None,
        special_features: dict = None,
        weaknesses: dict = None,
        damage: dict = None,
        stat_modifiers: dict = None,
    ) -> None:
        """
        Args:
            user_id (str): id пользователя в базе данных.
            db_source (DBSource): Объект класса базы данных.
            id (int): id листа персонажа в базе данных.
            name (str): Имя персонажа.
            race (str): Раса персонажа.
            character_class (str): Класс персонажа.
            stats (dict): Начальное распределение характеристик персонажа.
            hp (int): Начальное значение здоровья персонажа.
            allignment (str): Мировозрение персонажа.
            skills (dict): Навыки персонажа.
            weapons_and_equipment (dict): Оружие и снаряжение персонажа.
            ability_saving_throws (dict): Спасброски способностей персонажа.
            death_saving_throws (dict): Смертельные спасброски персонажа.
            attacks (dict): Атаки персонажа.
            spells (dict): Заклинания персонажа.
            passive_perception (int): Пассивное восприятие персонажа.
            traits_and_abilities (dict): Черты и способности персонажа.
            initiative (int): Инициатива персонажа.
            lvl (int): Уровень персонажа.
            speed (int): Скорость перемещения персонажа.
            backstory (str): Предыстория персонажа.
            experience (int): Опыт персонажа.
            valuables (dict): Ценности, принадлежащие персонажу.
            diary (str): Дневник персонажа.
            notes (str): Дополнительные заметки к персонажу.
            languages (dict): Языки, известные персонажу.
            npc_relations (dict): Отношения персонажа с NPC.
            inspiration (bool): Вдохновение персонажа.
            interference (bool): Вмешательство.
            ownership_bonus (int): Бонус владения персонажа.
            advantages (bool): Преимущества персонажа.
            attribute_points (int): Очки навыков персонажа.
            special_features (dict): Особые способности.
            weaknesses (dict): Слабости персонажа.
            damage (dict): Урон от атак персонажа.
            stat_modifiers (dict): Модификаторы к характеристикам персонажа.
        """
        self.user_id = user_id
        self.db_source = db_source
        self.id = id
        self.name = name
        self.race = race
        self.character_class = character_class
        self.stats = stats
        self.hp = hp
        self.alignment = alignment
        self.skills = skills
        self.weapons_and_equipment = weapons_and_equipment
        self.ability_saving_throws = ability_saving_throws
        self.death_saving_throws = death_saving_throws
        self.attacks = attacks
        self.spells = spells
        self.passive_perception = passive_perception
        self.traits_and_abilities = traits_and_abilities
        self.initiative = initiative
        self.lvl = lvl
        self.speed = speed
        self.backstory = backstory
        self.experience = experience
        self.valuables = valuables
        self.diary = diary
        self.notes = notes
        self.languages = languages
        self.npc_relations = npc_relations
        self.inspiration = inspiration
        self.interference = interference
        self.ownership_bonus = ownership_bonus
        self.advantages = advantages
        self.attribute_points = attribute_points
        self.special_features = special_features
        self.weaknesses = weaknesses
        self.damage = damage
        self.stat_modifiers = stat_modifiers
        self.table_name = "character_list"

    @function_log
    def insert(self) -> dict:
        """
        Сохранение листа персонажа в базу данных.

        Returns:
            dict: Словарь с данными листа персонажа.
        """
        if self.id:
            self.synchronize(self.id)
        else:
            insert_dict = self.__dict__()
            del insert_dict["id"]
            self.id = self.db_source.insert(self.table_name, insert_dict)[0]["id"]
        return self.__dict__()

    @function_log
    def update(self, dict: dict) -> List[dict]:
        """
        Изменение листа персонажа.

        Args:
            dict (dict): Словарь с новыми данными листа персонажа.

        Returns:
            List[dict]: Список из словаря с новой строкой.
        """
        data_list = self.db_source.update(self.table_name, dict, self.id)
        self.synchronize(self.id)
        return data_list

    @function_log
    def delete(self) -> List[dict]:
        """
        Удаление листа персонажа из базы данных.

        Returns:
            List[dict]: Список из словаря с удалённой строкой.
        """
        return self.db_source.delete(self.table_name, self.id)

    @function_log
    def get_by_id(self, id: int) -> List[dict]:
        """
        Получение листа персонажа по id.

        Args:
            id (str): id листа персонажа.
        
        Returns:
            List[dict]: Список из словаря со строкой таблицы.
        """
        return self.db_source.get_by_id(self.table_name, id)

    @function_log
    def get_by_value(self, parameter: str, parameter_value: any) -> List[dict]:
        """
        Получение листа персонажа по значению определенного параметра.

        Args:
            parameter (str): Столбец, по которому происходит сравнение.
            parameter_value (str / int / list): Значение, по которому происходит сравнение.

        Returns:
            List[dict]: Список из словаря со строкой таблицы.
        """
        return self.db_source.get_by_value(self.table_name, parameter, parameter_value)

    @function_log
    def synchronize(self, id: int) -> None:
        """
        Синхронизация объекта класса и данных в таблицах.

        Returns:
            id (int): id листа персонажа в таблице.
        """
        data_list = self.get_by_id(id)
        if len(data_list) == 0:
            self.insert()
        else:
            data_dict = data_list[0]
            self.set_attributes(data_dict)

    @function_log
    def __dict__(self) -> dict:
        """
        Вывод всех параметров листа персонажа в формате словаря.

        Returns:
            dict: Словарь с данными листа персонажа.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "race": self.race,
            "character_class": self.character_class,
            "stats": self.stats,
            "hp": self.hp,
            "alignment": self.alignment,
            "skills": self.skills,
            "weapons_and_equipment": self.weapons_and_equipment,
            "ability_saving_throws": self.ability_saving_throws,
            "death_saving_throws": self.death_saving_throws,
            "attacks": self.attacks,
            "spells": self.spells,
            "passive_perception": self.passive_perception,
            "traits_and_abilities": self.traits_and_abilities,
            "initiative": self.initiative,
            "lvl": self.lvl,
            "speed": self.speed,
            "backstory": self.backstory,
            "experience": self.experience,
            "valuables": self.valuables,
            "diary": self.diary,
            "notes": self.notes,
            "languages": self.languages,
            "npc_relations": self.npc_relations,
            "inspiration": self.inspiration,
            "interference": self.interference,
            "ownership_bonus": self.ownership_bonus,
            "advantages": self.advantages,
            "attribute_points": self.attribute_points,
            "special_features": self.special_features,
            "weaknesses": self.weaknesses,
            "damage": self.damage,
            "stat_modifiers": self.stat_modifiers,
        }

    @function_log
    def set_attributes(self, attr_dict: dict) -> None:
        """
        Установка параметров листа персонажа, заданных в словаре.

        Args:
            attr_dict (dict): Словарь с параметрами, которые нужно установить листу персонажа.
        """
        for key in attr_dict:
            setattr(self, key, attr_dict[key])
