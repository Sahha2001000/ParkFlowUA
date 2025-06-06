from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.card import Card

class CardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Card
        load_instance = True

card_schema = CardSchema()
cards_schema = CardSchema(many=True)
