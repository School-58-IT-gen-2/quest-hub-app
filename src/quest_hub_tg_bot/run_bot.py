import asyncio
import sys
sys.path.append("./src")   
import logging
from aiogram import Bot, Dispatcher, types
import os
from dotenv import load_dotenv
from aiogram.filters.command import Command
from adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.settings import envirements
import random
load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(envirements.BOT_TOKEN.get_secret_value())
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    supa = DBSource(url=envirements.SUPABASE_URL, key=envirements.SUPABASE_KEY)
    supa.connect()
    
    user = supa.get_by_value(table_name="profiles",parameter="tg_id",parameter_value=user_id)
    print(user)
    if user != []:
        await message.answer(f"С возвращением Великий {message.from_user.first_name}! Мы долго вас ждали для поисков приключений...")
    else:
        supa.insert(table_name="profiles",insert_dict={"first_name":message.from_user.first_name,
                                                       "last_name":message.from_user.last_name,
                                                       "tg_id":user_id,
                                                       "username":f"Великий {message.from_user.first_name}"})
        await message.answer(f"О приветствуем Вас, Лорд {message.from_user.first_name} {random.randint(1,15)}. Вы подписали контракт и теперь вы у нас в архивах... Не желаете ли начать поиски приключений?")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())