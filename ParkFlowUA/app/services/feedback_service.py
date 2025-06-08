from app.models import db
from app.models.feedback import Feedback
from loguru import logger

def save_feedback(feedback: Feedback):
    try:
        db.session.add(feedback)
        db.session.commit()
        logger.success(f"[FEEDBACK_SERVICE] Збережено фідбек: {feedback}")
    except Exception as e:
        db.session.rollback()
        logger.exception(f"[FEEDBACK_SERVICE] ❌ Помилка при збереженні: {e}")
        raise

def get_all_feedbacks():
    try:
        feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
        logger.debug(f"[FEEDBACK_SERVICE] Отримано {len(feedbacks)} фідбеків")
        return feedbacks
    except Exception as e:
        logger.exception(f"[FEEDBACK_SERVICE] ❌ Помилка при отриманні: {e}")
        return []
