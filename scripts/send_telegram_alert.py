from aiogram import Bot
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('ALERT_TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('ALERT_TELEGRAM_CHAT_ID') 
THREAD_ID = os.getenv('ALERT_THREAD_ID')  
MESSAGE_TEXT = "Healthcheck failed: Deploy project on server workflow in master"


if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, MESSAGE_TEXT]):
    raise ValueError("Не все переменные окружения заданы!")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_alert():
    try:
        if THREAD_ID:
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=MESSAGE_TEXT,
                message_thread_id=int(THREAD_ID) 
            )
        else:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=MESSAGE_TEXT)
        print("Сообщение успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(send_alert())