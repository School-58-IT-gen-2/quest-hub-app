class CharacterList:
    """Класс листа персонажа"""

    def __init__(self, id: str, name: str = None, race: str = None, character_class: str = None, stats: dict = None, hp: int = None, alignment: str = None, skills: dict = None, weapons_and_equipment: dict = None, ability_saving_throws: int = None, death_saving_throws: int = None, attacks: dict = None, spells: dict = None, passive_perception: int = None, traits_and_abilities: dict = None, initiative: int = None, lvl: int = None, speed: int = None, backstory: str = None, experience: int = None, valuables: dict = None, diary: str = None, notes: str = None, languages: dict = None, npc_relations: dict = None, inspiration: int = None, interference: bool = None, ownership_bonus: int = None, advantages: bool = None, attribute_points: int = None, special_fours: dict = None, weaknesses: dict = None, damage: dict = None, stat_modifiers: dict = None):
        """
        :param str id: id пользователя в базе данных
        :param str name: Имя персонажа
        :param str race: Раса персонажа
        :param str character_class: Класс персонажа
        :param dict stats: Начальное распределение характеристик персонажа
        :param int hp: Начальное значение здоровья персонажа
        :param str allignment: Мировозрение персонажа
        :param dict skills: Навыки персонажа
        :param dict weapons_and_equipment: Оружие и снаряжение персонажа
        :param int ability_saving_throws: Спасброски способностей персонажа
        :param int death_saving_throws: Смертельные спасброски персонажа
        :param dict attacks: Атаки персонажа
        :param dict spells: Заклинания персонажа
        :param int passive_perception: Пассивное восприятие персонажа
        :param dict traits_and_abilities: Черты и способности персонажа
        :param int initiative: Инициатива персонажа
        :param int lvl: Уровень персонажа
        :param int speed: Скорость перемещения персонажа
        :param str backstory: Предыстория персонажа
        :param int experience: Опыт персонажа
        :param dict valuables: Ценности, принадлежащие персонажу
        :param str diary: Дневник персонажа
        :param str notes: Дополнительные заметки к персонажу
        :param dict languages: Языки, известные персонажу
        :param dict npc_relations: Отношения персонажа с NPC
        :param int inspiration: Вдохновение персонажа ?????
        :param bool interference: ?????
        :param int ownership_bonus: ?????
        :param bool advantages: Преимущества персонажа ?????
        :param int attribute_points: ?????
        :param dict special_fours: ?????
        :param dict weaknesses: Слабости персонажа ?????
        :param dict damage: Урон от атак персонажа
        :param dict stat_modifiers: Модификаторы к характеристикам персонажа
        """
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
        self.special_fours = special_fours
        self.weaknesses = weaknesses
        self.damage = damage
        self.stat_modifiers = stat_modifiers
    
    def __dict__(self) -> dict:
        return {
            "id": self.id,
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
            "special_fours": self.special_fours,
            "weaknesses": self.weaknesses,
            "damage": self.damage,
            "stat_modifiers": self.stat_modifiers
        }