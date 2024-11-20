from adapters.db_source import DBSource
from model.user_model import User
from net_config import envirements

database = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
user = User('gsbd', 'hfjh', 'hbgdfb', [], 'fsvdg', 92365, database)

print(user.get_db_source())