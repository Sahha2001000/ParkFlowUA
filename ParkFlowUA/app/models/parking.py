from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import db

class City(db.Model):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    parkings = relationship("Parking", back_populates="city")

class Parking(db.Model):
    __tablename__ = 'parkings'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship("City", back_populates="parkings")
    spots = relationship("Spot", back_populates="parking")


class Spot(db.Model):
    __tablename__ = "parking_spots"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey("parkings.id"), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    hourly_rate = db.Column(db.Float, nullable=False, default=50.0)
    occupied_from = db.Column(db.DateTime, nullable=True)
    occupied_until = db.Column(db.DateTime, nullable=True)
    parking = db.relationship("Parking", back_populates="spots")
