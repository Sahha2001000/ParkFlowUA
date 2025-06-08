from app.models import db
from datetime import datetime
from loguru import logger
from sqlalchemy import event

class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "text": self.text,
            "timestamp": self.timestamp.isoformat()
        }

    def __repr__(self):
        return f"<Feedback(id={self.id}, user_id={self.user_id})>"

@event.listens_for(Feedback, "after_insert")
def log_insert(mapper, connection, target):
    logger.info(f"📝 Додано фідбек: {target}")
