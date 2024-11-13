import unittest
import os
from supabase_db_adapter import *
from dotenv import load_dotenv
load_dotenv()

class TestSupabaseAdapter(unittest.TestCase):
    def test_create_user(self):
        try:
            adapter = SupabaseDBAdapter(url=os.getenv("SUPABASE_URL"), key=os.getenv("SUPABASE_KEY")) 
            print("Successfully created adapter :)\n")
            adapter.create_new_user("test", 1)
            print("Successfully created users in table :)\n")
        except:
            self.fail("Failed to create users in table :(((")


    def test_get_user_data(self):
        try:
            adapter = SupabaseDBAdapter(url=os.getenv("SUPABASE_URL"), key=os.getenv("SUPABASE_KEY"))
            print("Successfully created adapter :)")
            user_data = adapter.get_user_data_by_id("test", 1)
            print("Successfully retrieved user data :)")
        except:
            self.fail("Failed to retrieve user data :(((")


    def test_update_user(self):
        try:
            adapter = SupabaseDBAdapter(url=os.getenv("SUPABASE_URL"), key=os.getenv("SUPABASE_KEY"))
            print("Successfully created adapter :)")
            adapter.update_user("test", 1)
            print("Successfully updated user data :)")
        except:
            self.fail("Failed to update user data :(((")



if __name__ == '__main__':
        unittest.main()

