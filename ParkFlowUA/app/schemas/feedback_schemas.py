from app.schemas import ma
from marshmallow import fields
from app.utils.logger import logger

class FeedbackSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    text = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)

feedback_schema = FeedbackSchema()
feedbacks_schema = FeedbackSchema(many=True)

logger.info("✅ Ініціалізовано FeedbackSchema")
