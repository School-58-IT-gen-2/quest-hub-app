import os
import logging
import asyncio
import sys
import traceback
from datetime import datetime, timezone, timedelta
from logging_loki import LokiHandler
# Настройка логирования
log_file = "app_activity.log"
log_separator = " ||| "  # Уникальный разделитель для удобного разбора логов

# Проверяем, существует ли файл, если нет — записываем заголовок
if not os.path.exists(log_file) or os.stat(log_file).st_size == 0:
    with open(log_file, "w") as f:
        f.write(
            "FORMAT: timestamp ||| level ||| function_name ||| context (args, kwargs) ||| result ||| error ||| error_code ||| traceback\n"
            "----------------------------------------------------------------------------------------------\n"
        )



'''logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(message)s",  # Отключаем стандартный формат, будем писать кастомные строки
)
'''
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# Создаем логгер
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)  # Уровень логирования

# --- 1. FileHandler (логи в файл) ---
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)  # Только INFO и выше
file_formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(file_formatter)

# --- 2. LokiHandler (логи в Grafana Loki) ---
loki_handler = LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"application": "my-app"},
    version="2"
)
loki_handler.setLevel(logging.INFO) 
loki_formatter = logging.Formatter("%(message)s")  # Можно настроить иначе
loki_handler.setFormatter(loki_formatter)

# Добавляем оба обработчика к логгеру
logger.addHandler(file_handler)
logger.addHandler(loki_handler)

# Функция удаления логов старше 30 дней
def delete_old_logs():
    try:
        with open(log_file, "r") as f:
            logs = f.readlines()

        one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
        new_logs = [logs[0], logs[1]]  # Сохраняем заголовки

        for log in logs[2:]:  # Пропускаем первые две строки с описанием формата
            try:
                timestamp_str = log.split(log_separator)[0]
                log_time = datetime.fromisoformat(timestamp_str)
                if log_time >= one_month_ago:
                    new_logs.append(log)
            except ValueError:
                continue  # Пропускаем строки с некорректным форматом времени

        with open(log_file, "w") as f:
            f.writelines(new_logs)

    except Exception as e:
        logger.error(f"Ошибка при удалении старых логов: {e}")

# Функция записи логов в файл
def log_to_file(level, function_name, context, result=None, error=None, error_code=None, traceback_info=None):
    timestamp = datetime.now(timezone.utc).isoformat()
    log_message = f"{timestamp}{log_separator}{level}{log_separator}{function_name}{log_separator}{context}{log_separator}{result if result is not None else ''}{log_separator}{error if error else ''}{log_separator}{error_code if error_code else ''}{log_separator}{traceback_info if traceback_info else ''}\n"
    if level == "INFO":
        logger.info(log_message)
    elif level == "ERROR":
        logger.error(log_message)

# Декоратор логирования
def function_log(func):
    async def async_wrapper(*args, **kwargs):
        context = f"{args}, {kwargs}"
        try:
            result = await func(*args, **kwargs)
            log_to_file("INFO", func.__name__, context, result=result)
            return result
        except Exception as e:
            error_type = e.__class__.__name__  # Получаем название ошибки (например, ValueError)
            tb = traceback.TracebackException.from_exception(e)
            traceback_info = "".join(tb.format())  # Чистая трассировка ошибки без декоратора
            log_to_file("ERROR", func.__name__, context, error=str(e), error_code=error_type, traceback_info=traceback_info)
            return None

    def sync_wrapper(*args, **kwargs):
        context = f"{args}, {kwargs}"
        try:
            result = func(*args, **kwargs)
            log_to_file("INFO", func.__name__, context, result=result)
            return result
        except Exception as e:
            error_type = e.__class__.__name__
            tb = traceback.TracebackException.from_exception(e)
            traceback_info = "".join(tb.format())
            log_to_file("ERROR", func.__name__, context, error=str(e), error_code=error_type, traceback_info=traceback_info)
            return None

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
