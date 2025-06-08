from app import create_app
from app.models import db, User, Parking, Booking
from datetime import datetime, timedelta, UTC
from werkzeug.security import generate_password_hash
from app.utils.logger import logger

# Ініціалізація додатку і контексту
app = create_app()
with app.app_context():
    logger.info("Створення таблиць у базі даних...")
    db.drop_all()
    db.create_all()

    db.session.commit()
    logger.success("Таблиці створено і тестові дані додано.")

    # cd C:\Users\OVasyliev\PycharmProjects\ParkFlowUA
    # python -m app.init_db

