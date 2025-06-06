from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate

from app.config import Config
import os

# Завантаження змінних середовища з .env
load_dotenv()

from app.models import db
from app.schemas import ma
from app.controllers import (
    auth_bp,
    user_bp,
    parking_bp,
    health_bp,
    car_bp,
    booking_bp,
    card_bp
)
from app.utils.logger import logger  # Імпорт логера

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ініціалізація бази даних та Marshmallow
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Реєстрація blueprint'ів
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(parking_bp)
    app.register_blueprint(car_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(card_bp)

    logger.info("Flask-додаток успішно ініціалізовано")
    return app
