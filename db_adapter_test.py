from adapters.db_source import DBSource
from net_config import envirements

database = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
database.connect()
print(database.delete('test', 17))