# app/utils/logger.py

from loguru import logger
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Додаємо обробник логів у файл
logger.add(
    os.path.join(LOG_DIR, "app.log"),
    rotation="1 MB",     # розділення файлів логів при досягненні 1MB
    retention="10 days", # зберігати до 10 днів
    compression="zip",   # архівувати старі логи
    level="INFO"
)

# Цей логер можна імпортувати у будь-який модуль
