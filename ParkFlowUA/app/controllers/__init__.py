from .auth_controller import auth_bp
from .user_controller import user_bp
from .parking_controller import parking_bp
from .health_controller import health_bp
from .car_controller import car_bp
from .booking_controller import booking_bp
from .card_controller import card_bp
from .feedback_controller import feedback_bp

from app.utils.logger import logger

# Логування ініціалізації контролерів
logger.info("Імпортовано контролери: auth, user, parking, health, car, booking, card, feedback")

__all__ = [
    'auth_bp',
    'user_bp',
    'parking_bp',
    'health_bp',
    'car_bp',
    'booking_bp',
    'card_bp',
    'feedback_bp'
]
