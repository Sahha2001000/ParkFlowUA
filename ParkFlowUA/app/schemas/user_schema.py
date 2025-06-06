from app.schemas import ma
from marshmallow import fields
from app.utils.logger import logger


class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)  # Не відображається при відповіді
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# Екземпляри для серіалізації
user_schema = UserSchema()
users_schema = UserSchema(many=True)

logger.info("Схема UserSchema ініціалізована")
