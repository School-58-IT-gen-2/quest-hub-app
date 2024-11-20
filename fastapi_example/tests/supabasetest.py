import unittest
import os
from fastapi_example.fastapi_example.adapters.supabase import *
from dotenv import load_dotenv
import time
from datetime import datetime,timezone
load_dotenv()

class TestSupabaseAdapter(unittest.TestCase):
    def test_select_user(self):
        try:
            supa = get_supabase_client()
            self.assertIsNotNone(supa.table("test").select("*").eq("id",1).execute())
        except:
            self.fail("Failed to select user :(")

    def test_create_user(self):
        try:
            supa = get_supabase_client()
            len1 = len(supa.table("test").select("*").execute())
            new_user = {    
                "id": int(time.time()),
                "created_at": str(datetime.now(timezone.utc)),
                "test": "test",
                "test2": 123
            }
            supa.table("test").insert(new_user).execute()
            len2 = len(supa.table("test").select("*").execute())
            self.assertNotEqual(len1,len2)
        except:
            self.fail("Failed to create user :(")   

    def test_update_user(self):
        try:
            supa = get_supabase_client()
            user_old = supa.table("test").select("*").eq("id",1).execute()
            supa.table("test").update({"created_at": str(datetime.now(timezone.utc))}).eq("id", id).execute()
            user_new = supa.table("test").select("*").eq("id",1).execute()
            self.assertNotEqual(user_old,user_new)
        except:
            self.fail("Failed to update user info :(")




if __name__ == '__main__':
    unittest.main()

