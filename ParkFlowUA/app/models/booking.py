from app.models import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)  # нове поле

    duration_hours = db.Column(db.Float, nullable=False, default=1.0)
    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)

