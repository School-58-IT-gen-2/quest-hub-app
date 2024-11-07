from supabase.client import ClientOptions
from supabase import create_client, Client

from fastapi_example.modules.settings import settings


def get_supabase_client():
    try:
        supabase: Client = create_client(
            supabase_url=settings.supabase.url,
            supabase_key=settings.supabase.key.get_secret_value(),
            options=ClientOptions(
                postgrest_client_timeout=10,
                storage_client_timeout=10,
                schema="public",
            ),
        )
        return supabase
    except Exception as error:
        print(f"Error: {error}")
        return error
