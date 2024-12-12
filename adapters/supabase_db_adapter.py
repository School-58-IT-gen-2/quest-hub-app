from supabase import create_client, Client
from datetime import datetime, timezone


class SupabaseDBAdapter:
    def __init__(self, url: str, key: str) -> None:
        supabase: Client = create_client(url, key)

    def get_user_data_by_id(table: str, id: int) -> list:
        user_data = supabase.table(table).select("*").eq("id", user_id).execute()
        return user_data.data

    def create_new_user(table: str, id: int) -> None:
        new_user = {"id": id, "created_at": str(datetime.now(timezone.utc))}

        supabase.table(table).insert(new_user).execute()

    def update_user(table: str, id: int) -> None:
        supabase.table(table).update(
            {"created_at": str(datetime.now(timezone.utc))}
        ).eq("id", id).execute()
