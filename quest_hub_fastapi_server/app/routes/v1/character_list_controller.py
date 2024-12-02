from fastapi import APIRouter, HTTPException
from model.character_list_model import CharacterList
from adapters.db_source import DBSource
from net_config import settings

route = APIRouter(prefix="/characters", tags=["characters"])

@route.post(path="/add")
def add_character(character: CharacterList):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        new_character = {
            "race": character.race,
            "character_class": character.character_class,
            "alignment": character.alignment,
            "backstory": character.backstory,
            "notes": character.notes,
            "diary": character.diary,
            "attribute_points": character.attribute_points,
            "hp": character.hp,
            "initiative": character.initiative,
            "lvl": character.lvl,
            "passive_perception": character.passive_perception,
            "speed": character.speed,
            "experience": character.experience,
            "ownership_bonus": character.ownership_bonus,
            "ability_saving_throws": character.ability_saving_throws,
            "death_saving_throws": character.death_saving_throws,
            "inspiration": character.inspiration,
            "interference": character.interference,
            "advantages": character.advantages,
            "weapons_and_equipment": character.weapons_and_equipment,
            "spells": character.spells,
            "traits_and_abilities": character.traits_and_abilities,
            "languages": character.languages,
            "attacks": character.attacks,
            "special_fours": character.special_fours,
            "weaknesses": character.weaknesses,
            "damage": character.damage,
            "npc_relations": character.npc_relations,
            "name": character.name,
            "valuables": character.valuables,
            "skills": character.skills,
            "stat_modifiers": character.stat_modifiers,
            "stats": character.stats,
            "user_id": character.user_id,
        }
        result = new_db_source.insert("character_list", new_character)
        if result:
            return result
        else:
            raise HTTPException(status_code=503, detail="Database unreachable")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error adding character")

@route.get(path="/{character_id}")
def get_character(character_id: int):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        character = new_db_source.get_by_id("character_list", character_id)
        if character:
            return character
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error retrieving character")

@route.put(path="/update/{character_id}")
def update_character(character_id: int, character: CharacterList):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        updated_character = {
            "race": character.race,
            "character_class": character.character_class,
            "alignment": character.alignment,
            "backstory": character.backstory,
            "notes": character.notes,
            "diary": character.diary,
            "attribute_points": character.attribute_points,
            "hp": character.hp,
            "initiative": character.initiative,
            "lvl": character.lvl,
            "passive_perception": character.passive_perception,
            "speed": character.speed,
            "experience": character.experience,
            "ownership_bonus": character.ownership_bonus,
            "ability_saving_throws": character.ability_saving_throws,
            "death_saving_throws": character.death_saving_throws,
            "inspiration": character.inspiration,
            "interference": character.interference,
            "advantages": character.advantages,
            "weapons_and_equipment": character.weapons_and_equipment,
            "spells": character.spells,
            "traits_and_abilities": character.traits_and_abilities,
            "languages": character.languages,
            "attacks": character.attacks,
            "special_fours": character.special_fours,
            "weaknesses": character.weaknesses,
            "damage": character.damage,
            "npc_relations": character.npc_relations,
            "name": character.name,
            "valuables": character.valuables,
            "skills": character.skills,
            "stat_modifiers": character.stat_modifiers,
            "stats": character.stats,
            "user_id": character.user_id,
        }
        result = new_db_source.update("character_list", updated_character, character_id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error updating character")

@route.delete(path="/delete/{character_id}")
def delete_character(character_id: int):
    try:
        new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
        new_db_source.connect()
        result = new_db_source.delete("character_list", character_id)
        if result:
            return {"detail": "Character deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Character not found")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error deleting character")