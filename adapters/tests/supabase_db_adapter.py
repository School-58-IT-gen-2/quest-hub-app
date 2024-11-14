from supabase import create_client, Client
from datetime import datetime, timezone
import supabase
import os
from dotenv import load_dotenv
load_dotenv()

class SupabaseDBAdapter :
    def __init__(self, url:str, key:str) -> None:
        self.supabase: Client = create_client(url, key)

    def get_user_data_by_id(self, table:str, id:int) -> list:
        user_data = self.supabase.table(table).select("*").eq("id", id).execute()
        return user_data.data
    
    def create_new_user(self, table:str, id:int) -> None:
        new_user = {
            "id": id,
            "created_at": str(datetime.now(timezone.utc)),
            "test": "test supabase",
            "test2": 123
        }

        self.supabase.table(table).insert(new_user).execute()

    def update_user(self, table:str, id:int) -> None:
        self.supabase.table(table).update({"created_at": str(datetime.now(timezone.utc))}).eq("id", id).execute()

    def get_all_users_data(self, table:str) -> list:
        user_data = self.supabase.table(table).select("*").execute()
        return user_data.data

