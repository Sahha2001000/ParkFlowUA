import os
from loguru import logger

class Config:
    # Загальні налаштування
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']
    TESTING = os.getenv('TESTING', 'False').lower() in ['true', '1', 'yes']
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')

    # SQLAlchemy (SQLite за замовчуванням)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///parkflow.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Додаткові параметри
    VERSION = os.getenv('VERSION', '1.0.0')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# Налаштування loguru
logger.remove()
logger.add(lambda msg: print(msg, end=""), level=Config.LOG_LEVEL)

# Логування конфігурації
logger.info("Конфігурація завантажена:")
logger.info(f"  DEBUG = {Config.DEBUG}")
logger.info(f"  TESTING = {Config.TESTING}")
logger.info(f"  SQLALCHEMY_DATABASE_URI = {Config.SQLALCHEMY_DATABASE_URI}")
logger.info(f"  VERSION = {Config.VERSION}")
logger.info(f"  LOG_LEVEL = {Config.LOG_LEVEL}")
