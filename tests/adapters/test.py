import sys
sys.path.append(".")
from adapters.db_source import DBSource
from dotenv import load_dotenv
import os
from datetime import datetime,timezone
load_dotenv()
supa = DBSource(url=os.getenv("SUPABASE_URL"),key=os.getenv("SUPABASE_KEY"))
supa.connect()
user_old = supa.get_by_id("test",15)
t = supa.update("test",{"created_at": str(datetime.now(timezone.utc))},15)
user_new = supa.get_by_id("test",15)
print(user_old)
print(t)
print(user_new)