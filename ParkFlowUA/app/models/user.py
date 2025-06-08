from app.models import db
from loguru import logger
from sqlalchemy import event

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(100))  # ← додай це
    password_hash = db.Column(db.String(255))  # ← і це, якщо плануєш логін через веб


    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, phone={self.phone_number})>"

# Логування після вставки нового запису
@event.listens_for(User, 'after_insert')
def log_user_insert(mapper, connection, target):
    logger.info(f"👤 Додано користувача в БД: {target}")
