# from adapters.db_source import DBSource
# from net_config import envirements

# database = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
# database.connect()

from abc import ABC

class Dog():
    @classmethod
    def get_name(cls):
        return cls.__name__

dogg = Dog()
print(dogg.get_name())