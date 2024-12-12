import sys

sys.path.append("./src")
import unittest
import time
from datetime import datetime, timezone
from adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import envirements


class TestSupabaseAdapter(unittest.TestCase):
    def test_get_all_users(self):
        try:
            supa = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
            supa.connect()
            self.assertIsNotNone(supa.get_all("test"))
        except:
            self.fail("Failed to get all :(")

    def test_get_by_id(self):
        try:
            supa = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
            supa.connect()
            self.assertIsNotNone(supa.get_by_id("test", 52))
        except:
            self.fail("Failed to get by id :(")

    def test_get_by_value(self):
        try:
            supa = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
            supa.connect()
            self.assertIsNotNone(supa.get_by_value("test", "test", "test"))
        except:
            self.fail("Failed to get by value :(")

    def test_insert(self):
        try:
            supa = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
            supa.connect()
            n1 = len(list(supa.get_all("test")))
            new_data = {
                "id": int(time.time()),
                "created_at": str(datetime.now(timezone.utc)),
                "test": "test",
                "test2": 123,
            }
            supa.insert("test", new_data)
            n2 = len(list(supa.get_all("test")))
            self.assertNotEqual(n1, n2)
        except:
            self.fail("Failed to insert :(")

    def test_update(self):
        try:
            supa = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
            supa.connect()
            u1 = supa.get_by_id("test", 16)[0]["created_at"]
            u2 = supa.update(
                "test", {"created_at": str(datetime.now(timezone.utc))}, 16
            )[0]["created_at"]
            self.assertNotEqual(u1, u2)
        except:
            self.fail("Failed to update :(")

    def test_delete(self):
        try:
            supa = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
            supa.connect()
            n1 = len(list(supa.get_all("test")))
            supa.delete("test", 52)
            n2 = len(list(supa.get_all("test")))
            supa.insert(
                "test",
                {
                    "id": 52,
                    "created_at": str(datetime.now(timezone.utc)),
                    "test": "test",
                    "test2": 123,
                },
            )
            self.assertNotEqual(n1, n2)
        except:
            self.fail("Failed to delete :(")


if __name__ == "__main__":
    unittest.main()
