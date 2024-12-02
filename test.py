from model.user_model import *
from net_config import envirements

db_source = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
db_source.connect()
user = User(9726598346987569278678945692736549, db_source, 'test')

print(user.insert())
print(user)