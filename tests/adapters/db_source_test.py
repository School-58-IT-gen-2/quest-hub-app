import sys
sys.path.append("./")
import unittest
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timezone
from adapters.db_source import DBSource

load_dotenv()

DBSource(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")).connect()

class TestSupabaseAdapter(unittest.TestCase):
    def test_select_user(self):
        try:
            supa = DBSource(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

            supa.connect()
            print(supa.get_all("test"))
            self.assertIsNotNone(supa.get_all("test"))
        except:
            self.fail("Failed to select user :(")

    def test_create_user(self):
        try:
            supa = DBSource(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
            supa.connect()
            len1 = len(supa.get_all())
            new_user = {
                "id": int(time.time()),
                "created_at": str(datetime.now(timezone.utc)),
                "test": "test",
                "test2": 123,
            }
            supa.insert("test", new_user)
            len2 = len(supa.get_all("test"))
            self.assertNotEqual(len1, len2)
        except:
            self.fail("Failed to create user :(")

    def test_update_user(self):
        try:
            supa = DBSource(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
            supa.connect()
            user_old = supa.get_by_id("test", 1)
            supa.update("test", {"created_at": str(datetime.now(timezone.utc))}, 1)
            user_new = supa.get_by_id("test", 1)
            self.assertNotEqual(user_old, user_new)
        except:
            self.fail("Failed to update user info :(")

    def test_delete_user(self):
        try:
            supa = DBSource(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
            supa.connect()
            len1 = len(supa.get_all("test"))
            supa.delete("test", 1)
            len2 = len(supa.get_all("test"))
            new_user = {
                "id": 1,
                "created_at": str(datetime.now(timezone.utc)),
                "test": "test",
                "test2": 123,
            }
            supa.insert("test", new_user)
            self.assertNotEqual(len1, len2)
        except:
            self.fail("Failed to update user info :(")


if __name__ == "__main__":
    unittest.main()
