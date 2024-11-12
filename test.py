from supabase import create_client, Client
from net_config import envirements
from pydantic import SecretStr

url: str = envirements.SUPABASE_URL
key: SecretStr = envirements.SUPABASE_KEY

supabase: Client = create_client(url, key.get_secret_value())

response = (
    supabase.from_("test")
    .insert(
        [
            {
                "test": 'test',
                "test2": 2
            }
        ]
    )
    .execute()
)

print(supabase.table("test").select().execute())

