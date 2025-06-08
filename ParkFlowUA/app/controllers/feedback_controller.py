from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import Feedback
from app.services.feedback_service import save_feedback, get_all_feedbacks
from app.schemas.feedback_schemas import feedback_schema, feedbacks_schema
from loguru import logger

feedback_bp = Blueprint("feedback", __name__, url_prefix="/api/feedback")

@feedback_bp.route("", methods=["POST"])
def create_feedback():
    try:
        data = request.get_json()
        logger.info(f"[FEEDBACK_CONTROLLER] POST: {data}")

        # Валідація
        errors = feedback_schema.validate(data)
        if errors:
            logger.warning(f"[FEEDBACK_CONTROLLER] ❌ Валідація не пройдена: {errors}")
            return jsonify({"errors": errors}), 400

        feedback = Feedback(
            user_id=data["user_id"],
            text=data["text"],
            timestamp=datetime.utcnow()
        )

        save_feedback(feedback)
        return jsonify({"status": "ok", "id": feedback.id}), 201

    except Exception as e:
        logger.exception("[FEEDBACK_CONTROLLER] ❌ Помилка при створенні фідбеку")
        return jsonify({"error": str(e)}), 500

@feedback_bp.route("", methods=["GET"])
def list_feedbacks():
    try:
        feedbacks = get_all_feedbacks()
        return jsonify(feedbacks_schema.dump(feedbacks)), 200
    except Exception as e:
        logger.exception("[FEEDBACK_CONTROLLER] ❌ Помилка при отриманні фідбеків")
        return jsonify({"error": str(e)}), 500
