from flask import Blueprint, jsonify
from app.services.health_service import get_health_status
from app.utils.logger import logger

health_bp = Blueprint("health", __name__)

@health_bp.route("/api/health", methods=["GET"])
def health_check():
    logger.info("Health check запит отримано")
    try:
        data = get_health_status()
        logger.info(f"Health check успішно виконано: {data}")
        return jsonify(data), 200
    except Exception as e:
        logger.exception("Помилка під час виконання health check")
        return jsonify({"status": "error", "message": str(e)}), 500
