from model.user_model import *
from net_config import envirements

db_source = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
db_source.connect()
user = User(98240956203984, db_source, 'jbvsodbfvosidbvihfbkb')
user.synchronize()

print(user.__dict__())
print('=====================================')
print(user.get_char_lists())
