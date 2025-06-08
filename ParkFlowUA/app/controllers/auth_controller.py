from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.services.user_service import get_user_by_username
from app.utils.logger import logger  # логер loguru

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    logger.info(f"Запит авторизації: username={username}")

    user = get_user_by_username(username)
    if not user:
        logger.warning(f"Користувача не знайдено: {username}")
        return jsonify({"error": "Користувача не знайдено"}), 404

    if not check_password_hash(user.password_hash, password):
        logger.warning(f"Невірний пароль для користувача: {username}")
        return jsonify({"error": "Невірний пароль"}), 401

    logger.info(f"Авторизація успішна для: {username}")
    return jsonify({
        "message": f"Вітаємо, {username}!",
        "user_id": user.id
    }), 200
