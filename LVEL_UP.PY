import requests
import json
import uuid
import g4f
from g4f import Client
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.modules.char_list.models import (
    CharListRequestModel,
    Note,Item,Spell,
    BadRequestException,
    InternalServerErrorException,
    ServiceUnavailableException
)

charlist = {
    "character_class": "Следопыт",
    "hp": 11,
    "initiative": 0,
    "lvl": 1,
    "passive_perception": 12,
    "speed": 25,
    "experience": 0,
    "ownership_bonus": 2,
    "death_saving_throws": 0,
    "spells": {},
    "traits_and_abilities": [
      {
        "id": "c35e6299-fb23-4bd7-bdcd-934a0dd4008f",
        "name": "Тёмное зрение",
        "description": "Привыкшие к жизни под землей, вы обладаете превосходным зрением в темноте и при тусклом свете. Вы можете видеть в тусклом свете на расстоянии до 60 футов, как при ярком свете, и в полной темноте, как при тусклом свете. Вы не различаете цвета в темноте, видя только оттенки серого."
      },
      {
        "id": "3698847c-3a73-4175-a6b1-f828fa20f9cc",
        "name": "Дворфийская стойкость",
        "description": "Вы имеете преимущество на спасброски от яда и сопротивление к урону ядом."
      },
      {
        "id": "3c6b8386-3996-4964-a319-3f857a25e2c8",
        "name": "Дворфийская боевая подготовка",
        "description": "Вы обладаете мастерством в боевом топоре, ручном топоре, лёгком молоте и боевом молоте."
      },
      {
        "id": "1abde649-9ad7-4908-8f88-0d134017078b",
        "name": "Мастерство в инструментах",
        "description": "Вы получаете мастерство в одном из следующих наборов инструментов: кузнечные инструменты, пивоваренное оборудование или каменщик."
      },
      {
        "id": "ad5cacbf-9f13-419c-90da-832fd213de5b",
        "name": "Чувство камня",
        "description": "Когда вы делаете проверку Истории, связанную с каменной кладкой, вы считаете себя мастером этого навыка и добавляете удвоенный бонус мастерства вместо обычного."
      },
      {
        "id": "22bfc49e-4915-4f35-9b90-051ec532d4b3",
        "name": "Дворфийское обучение броне",
        "description": "Вы обладаете мастерством в легких и средних доспехах."
      }
    ],
    "skills": [
      "Внимание",
      "Атлетика",
      "Выживание",
      "Природа",
      "Анализ",
      "Скрытность",
      "Акробатика"
    ],
    "stat_modifiers": {
      "strength": -1,
      "dexterity": 2,
      "constitution": 1,
      "intelligence": 1,
      "wisdom": 2,
      "charisma": 1
    },
    "stats": {
      "strength": 8,
      "dexterity": 15,
      "constitution": 12,
      "intelligence": 12,
      "wisdom": 15,
      "charisma": 13
    },
    "ability_saving_throws": {
      "strength": -1,
      "dexterity": 2
    },
    "subrace": "Холмовой дворф",
    "gender": "M",
    "archetype": None,
  }
def ask_g4f(question, model="gpt-3.5-turbo"):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": question}],
    )
    return response

def claude(question, model="gpt-3.5-turbo"):
    response = g4f.ChatCompletion.create(
        model=g4f.models.claude_3_7_sonnet,
        messages=[{"role": "user", "content": question}],
    )
    return response

def deepseek(question, model="gpt-3.5-turbo"):
    response = g4f.ChatCompletion.create(
        model=g4f.models.deepseek_v3,
        messages=[{"role": "user", "content": question}],
    )
    return response

class Prompt(BaseModel):
    question: str

class Char(BaseModel):
    char: dict

def what_to_choose(charlist:dict):
    # res = "Представь, что ты профессиональный игрок в D&D и хорошо разбираешься в механике игры,опирайся на данные с этого сайта  https://dnd.su/class/99-rogue/. У меня есть персонаж, которому нужно повысить уровень. Все данные о нём приведены в формате JSON далее. Проанализируй их и скажи мне,какие данные мне надо предоставить,чтобы корректно повысить уровень персонажа на 1 вверх.Если надо выбрать архетип или умение,то дай мне варианты выбора.ТЫ не должен ничего мне рекомендоавать,только дать варианты выбора.Предоставь ВСЕ варианты выбора в формате: '<характеристика,которую надо выбрать1:вариант1,вариант2,вариант3>,<характеристика,которую надо выбрать1:вариант1,вариант2,вариант3>,<характеристика,которую надо выбрать1:вариант1,вариант2,вариант3>'.Если ничего выбирать не надо,то верни <Я могу повысить уровень!> Вот данные о персонаже:" + str(json.dumps(char.char, ensure_ascii=False)) + " "
    res = "Представь, что ты профессиональный игрок в D&D и хорошо разбираешься в механике игры,делай все строго,как написано на этом сайте https://dnd.su/class/,там есть вкладки со всеми классами,например для следопыта https://dnd.su/class/97-ranger/.Архетип выбирается только на третьем уровне.В случае следопыта при повышении на 2 уровень ты должен вернуть: '<Боевой стиль: Дуэлянт,Оборона,Сражение двумя оружиями,Стрельба,Сражение вслепую,Воин-друид' У меня есть персонаж, которому нужно повысить уровень. Все данные о нём приведены в формате JSON далее. Проанализируй их и скажи мне,какие данные мне надо предоставить,чтобы корректно повысить уровень персонажа до 2.Если надо выбрать архетип или умение,то дай мне варианты выбора.ТЫ не должен ничего мне рекомендоавать,только дать варианты выбора. Вот данные о персонаже:" + str(charlist) + "Я буду использовать твой ответ в скрипте python.Поэтому верни мне данные строго в формате: 'что выбираем(архетип,умение,характеристика и тд):вариант выбора 1,вариант выбора 2,вариант выбора 3 и тд|что выбираем(архетип,умение,характеристика и тд):вариант выбора 1,вариант выбора 2,вариант выбора 3 и тд',соблюдай этот формат и различные выборы разделяй с помощью '|'.Кроме этого ничего не возвращай"
    response = deepseek(res)
    print(response)
    return response

def choose(response):
    response = response.split('|')
    choose_dict = {}
    for i in response:
        i = i.split(":")
        choose_dict[i[0]] = i[1].split(",")
    print(choose_dict)
    result = ''
    for i in list(choose_dict.keys()):
        result += input(f"Выберете {i} из этих вариантов: {choose_dict[i]}")
    return result
def level_up(charlist:dict,choices:str):
    res = f"Представь, что ты профессиональный игрок в D&D и хорошо разбираешься в механике игры,опирайся на данные с этого сайта  https://dnd.su/class/99-rogue/. У меня есть персонаж, которому нужно повысить уровень. Все данные о нём приведены в формате JSON ниже. Проанализируй их и повысь уровень моего персонажа до 2.Вот данные,которые пригодятся тебе при повышении:{choices}.Верни ТОЛЬКО json в таком же формате что я тебе дал,ты можешь добавлять новые поля,если тебе надо внести информацию, но не можешь изменять старые,который я смогу использовать в коде.Кроме JSON ничего не возвращай.Вот json с данными о персонаже:" + str(charlist)
    response = deepseek(res)
    return response
    

print(level_up(charlist,choose(what_to_choose(charlist=charlist)))) 