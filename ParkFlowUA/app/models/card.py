# app/models/card.py
from app.models import db

class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    number = db.Column(db.String(16), nullable=False)  # <-- ЦЕ ВАЖЛИВО
    exp_date = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
