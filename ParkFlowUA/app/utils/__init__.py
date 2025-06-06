# Позначає папку utils як Python-модуль
# Для імпорту спільних утиліт (логер, тощо)

from .logger import logger


logger.info("Утиліти ініціалізовано: logger")

__all__ = [
    'logger'
]
