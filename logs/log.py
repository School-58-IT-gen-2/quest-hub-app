import os
import time
import functools
import sys
import traceback
import asyncio
from datetime import datetime, timezone, timedelta
from supabase import create_client, Client

# Подключение к базе данных Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Функция для удаления логов старше 30 дней
async def delete_old_logs():
    one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)  # Вычисляем дату 30 дней назад
    response = supabase.table("logs").select("id, timestamp").execute()  # Запрашиваем все логи из базы данных
    
    if response.data:
        for record in response.data:
            log_time = datetime.fromisoformat(record["timestamp"])  # Преобразуем строку в объект datetime
            if log_time < one_month_ago:  # Если запись старше 30 дней, удаляем её
                supabase.table("logs").delete().eq("id", record["id"]).execute()

# Асинхронная функция для отправки логов в Supabase
async def log_to_supabase(data):
    await delete_old_logs()  # Удаляем старые логи перед добавлением нового
    await asyncio.to_thread(supabase.table("logs").insert(data).execute)  # Вставляем новый лог в базу данных

# Декоратор для логирования с обработкой ошибок
def function_log(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        timestamp = datetime.now(timezone.utc).isoformat()  # Фиксируем текущее время
        function_name = func.__name__  # Получаем имя декорируемой функции
        level = "INFO"  # По умолчанию уровень логирования INFO
        context = {"args": args, "kwargs": kwargs}  # Записываем переданные аргументы

        try:
            result = await func(*args, **kwargs)  # Выполняем асинхронную функцию
            message = f"Функция {function_name} выполнена успешно"
        except Exception as e:
            level = "ERROR"  # При ошибке меняем уровень логирования на ERROR
            message = f"Ошибка в {function_name}: {str(e)}"  # Формируем сообщение об ошибке
            error_type, error_value, error_traceback = sys.exc_info()  # Получаем информацию об ошибке
            error_trace = "".join(traceback.format_tb(error_traceback))  # Форматируем трассировку ошибки
            context.update({
                "error_type": str(error_type),
                "error_message": str(error_value),
                "error_trace": error_trace
            })
            await log_to_supabase({"timestamp": timestamp, "level": level, "message": message, "context": context})
            return None  # Возвращаем None в случае ошибки

        await log_to_supabase({"timestamp": timestamp, "level": level, "message": message, "context": context})
        return result  # Возвращаем результат работы функции

    def sync_wrapper(*args, **kwargs):
        timestamp = datetime.now(timezone.utc).isoformat()  # Фиксируем текущее время
        function_name = func.__name__  # Получаем имя функции
        level = "INFO"  # По умолчанию уровень INFO
        context = {"args": args, "kwargs": kwargs}  # Записываем аргументы функции

        try:
            result = func(*args, **kwargs)  # Выполняем синхронную функцию
            message = f"Функция {function_name} выполнена успешно"
        except Exception as e:
            level = "ERROR"  # Если произошла ошибка, меняем уровень логирования
            message = f"Ошибка в {function_name}: {str(e)}"
            error_type, error_value, error_traceback = sys.exc_info()
            error_trace = "".join(traceback.format_tb(error_traceback))
            context.update({
                "error_type": str(error_type),
                "error_message": str(error_value),
                "error_trace": error_trace
            })
            asyncio.ensure_future(log_to_supabase({"timestamp": timestamp, "level": level, "message": message, "context": context}))
            return None  # Возвращаем None при ошибке

        asyncio.ensure_future(log_to_supabase({"timestamp": timestamp, "level": level, "message": message, "context": context}))
        return result  # Возвращаем результат функции

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper  # Определяем, какую версию использовать


