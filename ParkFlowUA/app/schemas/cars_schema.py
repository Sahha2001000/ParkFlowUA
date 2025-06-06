from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Car

class CarSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Car
        load_instance = True
        include_fk = True  # дозволяє включити зовнішній ключ user_id

# Один об'єкт
car_schema = CarSchema()

# Список об'єктів
cars_schema = CarSchema(many=True)
