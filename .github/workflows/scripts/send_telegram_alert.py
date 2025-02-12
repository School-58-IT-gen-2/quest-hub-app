from aiogram import Bot
import asyncio
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
MESSAGE_TEXT = os.getenv('MESSAGE_TEXT')

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_alert():
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=MESSAGE_TEXT)

if __name__ == '__send_telegram_alert.py__':
    asyncio.run(send_alert())