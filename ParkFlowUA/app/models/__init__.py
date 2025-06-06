from flask_sqlalchemy import SQLAlchemy

# Ініціалізація об'єкта бази даних
db = SQLAlchemy()

# Імпортуємо всі моделі після ініціалізації db
from .user import User
from .parking import Parking
from .car import Car
from .booking import Booking
from .card import Card

# Логування факту імпорту моделей
from app.utils.logger import logger
logger.info("Ініціалізовано моделі: User, Parking, Spot, Car, Booking, Card")

# Експорт для зовнішнього використання
__all__ = ['db', 'User', 'Booking', 'Parking', 'Car', 'Card']
