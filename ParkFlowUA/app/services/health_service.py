from datetime import datetime, timezone
import socket
import logging
from app.config import Config

logger = logging.getLogger(__name__)

def get_health_status():
    logger.info("[HEALTH_SERVICE] Початок формування health check відповіді")
    try:
        data = {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "host": socket.gethostname(),
            "version": Config.VERSION
        }
        logger.info(f"[HEALTH_SERVICE] Дані успішно сформовано: {data}")
        return data
    except Exception as e:
        logger.exception("[HEALTH_SERVICE] Помилка при формуванні health status")
        raise
