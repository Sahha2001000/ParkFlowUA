from app.models import db


class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ← важливо!
    brand = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(16), nullable=False, unique=True)

    user = db.relationship('User', backref='cars')  # ← зворотне посилання
