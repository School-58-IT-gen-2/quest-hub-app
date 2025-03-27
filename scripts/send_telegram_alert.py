from aiogram import Bot
import asyncio
import os
from dotenv import load_dotenv
from aiogram.exceptions import TelegramRetryAfter

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') 
THREAD_ID = os.getenv('THREAD_ID')  
MESSAGE_TEXT = "Healthcheck failed: Deploy project on server workflow in master"


if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, MESSAGE_TEXT]):
    raise ValueError("Не все переменные окружения заданы!")

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_alert():
    try:
        if THREAD_ID:
            await bot.send_message(
                chat_id=int(TELEGRAM_CHAT_ID),
                text=MESSAGE_TEXT,
                message_thread_id=int(THREAD_ID) 
            )
        else:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=MESSAGE_TEXT)
        print("Сообщение успешно отправлено!")
    except TelegramRetryAfter as e:
        print(f"Превышен лимит запросов. Повторная попытка через {e.retry_after} секунд.")
        await asyncio.sleep(e.retry_after)
        await send_alert()  # Повторная попытка отправки
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(send_alert())