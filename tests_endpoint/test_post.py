import unittest
import subprocess
import time
import httpx
import sys
from pathlib import Path

# Добавляем путь к проекту в PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

class TestAPIEndpoints(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Запуск сервера в фоне
        cls.server_process = subprocess.Popen(
            ["uvicorn", "quest_hub_fastapi_server.app:app", "--host", "0.0.0.0", "--port", "9009"]
        )
        # Ждем 3 секунды для инициализации сервера
        time.sleep(3)

    def setUp(self):
        self.local = "https://questhub.pro"

    @classmethod
    def tearDownClass(cls):
        # Останавливаем сервер
        cls.server_process.terminate()

    async def test1_create_user(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.local}/api/v1/characters/char-list",
                json={
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "race": "string",
  "character_class": "string",
  "backstory": "string",
  "notes": {
    "title": "string",
    "text": "string",
    "id": "string"
  },
  "hp": 0,
  "initiative": 0,
  "lvl": 0,
  "passive_perception": 0,
  "speed": 0,
  "experience": 0,
  "ownership_bonus": 0,
  "ability_saving_throws": {},
  "death_saving_throws": 0,
  "interference": True,
  "advantages": True,
  "weapons_and_equipment": [
    {
      "id": "string",
      "count": 1,
      "type": "string",
      "name": "string",
      "description": "string",
      "weight": 0,
      "cost": 0,
      "damage": "string",
      "damage_type": "string",
      "properties": [
        "string"
      ],
      "ac_base": 0,
      "dex_bonus": True,
      "max_dex_bonus": 0,
      "stealth_disadvantage": True
    }
  ],
  "spells": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "range": "string",
      "duration": "string",
      "casting_time": "string",
      "components": "string"
    }
  ],
  "traits_and_abilities": [
    {
      "id": "string",
      "name": "string",
      "description": "string"
    }
  ],
  "languages": [
    "string"
  ],
  "special_features": {},
  "weaknesses": {},
  "npc_relations": {},
  "name": "string",
  "gold": 0,
  "skills": [
    "string"
  ],
  "stat_modifiers": {},
  "stats": {},
  "user_id": "string",
  "inspiration": True,
  "surname": "string",
  "inventory": [
    {
      "id": "string",
      "count": 1,
      "type": "string",
      "name": "string",
      "description": "string",
      "weight": 0,
      "cost": 0,
      "damage": "string",
      "damage_type": "string",
      "properties": [
        "string"
      ],
      "ac_base": 0,
      "dex_bonus": True,
      "max_dex_bonus": 0,
      "stealth_disadvantage": True
    }
  ],
  "age": 0,
  "worldview": "string",
  "subrace": "string",
  "gender": "string"
}
            )
            self.assertEqual(response.status_code, 200)

    async def test_profile_user(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.local}/api/v1/profiles/user",
                json={
  "tg_id": 0,
  "first_name": "string",
  "role": "player",
  "is_bot": True,
  "username": "string",
  "age": 0,
  "last_name": "string",
  "is_premium": True,
  "language_code": "string"
}
            )
            self.assertEqual(response.status_code, 200)



    async def test_get_prof(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.local}/api/v1/profiles/profile",
              params={"tg_id": 0}
            )
            self.assertEqual(response.status_code, 200)


    async def test_get_games(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.local}/api/v1/games/create",
                json={
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "string",
  "description": "string",
  "created_at": "2025-04-23T17:28:20.986Z",
  "is_online": True,
  "place": "string",
  "game_level": "легко",
  "number_of_players": 0,
  "master_id": "string",
  "players_id": [
    "string"
  ],
  "seed": "string"
}
            )
            responsedata = response.json()
            id = responsedata["id"]
            self.assertEqual(response.status_code, 201)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.local}/api/v1/games/view_game",
              params={"game_id": id}
            )
            self.assertEqual(response.status_code, 200)

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.local}/api/v1/games/update_game",
              json={"id": id, "name": "Vsem privet! Ya Telepuzik))"}
            )
            self.assertEqual(response.status_code, 200)

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.local}/api/v1/games/delete_game",
              params={"game_id": id}
            )
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

