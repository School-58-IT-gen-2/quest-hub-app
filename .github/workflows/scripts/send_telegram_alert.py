from aiogram import Bot
import asyncio
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') 
THREAD_ID = os.getenv('THREAD_ID')  
MESSAGE_TEXT = os.getenv('MESSAGE_TEXT')

if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, MESSAGE_TEXT]):
    raise ValueError("Не все переменные окружения заданы!")

# Инициализируем бота
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