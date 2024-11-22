from adapters.db_source import DBSource
from model.user_model import User
from net_config import envirements

database = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
database.connect()
user = User(923645, database, 'test2')
