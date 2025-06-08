from app.models import User, db
from werkzeug.security import generate_password_hash
from app.utils.logger import logger


def get_all_users():
    logger.info("[USER SERVICE] Отримання всіх користувачів")
    users = User.query.all()
    return [u.to_dict() for u in users]


def get_user_by_id(user_id):
    logger.info(f"[USER SERVICE] Пошук користувача за ID={user_id}")
    user = User.query.get(user_id)
    return user.to_dict() if user else None


def get_user_by_username(username):
    logger.debug(f"[USER SERVICE] Пошук користувача за username='{username}'")
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    logger.debug(f"[USER SERVICE] Пошук користувача за email='{email}'")
    return User.query.filter_by(email=email).first()


def create_user(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if get_user_by_username(username):
        logger.warning(f"[USER SERVICE] Користувач з username '{username}' вже існує")
        return None
    if get_user_by_email(email):
        logger.warning(f"[USER SERVICE] Користувач з email '{email}' вже існує")
        return None

    try:
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        logger.success(f"[USER SERVICE] Користувач '{username}' створений")
        return new_user.to_dict()
    except Exception as e:
        logger.error(f"[USER SERVICE] Помилка створення користувача: {e}")
        db.session.rollback()
        return None


def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        logger.warning(f"[USER SERVICE] Користувача ID={user_id} не знайдено для оновлення")
        return False

    try:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        logger.success(f"[USER SERVICE] Користувач ID={user_id} оновлений")
        return True
    except Exception as e:
        logger.error(f"[USER SERVICE] Помилка оновлення користувача: {e}")
        db.session.rollback()
        return False


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        logger.warning(f"[USER SERVICE] Користувача ID={user_id} не знайдено для видалення")
        return False

    try:
        db.session.delete(user)
        db.session.commit()
        logger.success(f"[USER SERVICE] Користувач ID={user_id} видалений")
        return True
    except Exception as e:
        logger.error(f"[USER SERVICE] Помилка видалення користувача: {e}")
        db.session.rollback()
        return False
