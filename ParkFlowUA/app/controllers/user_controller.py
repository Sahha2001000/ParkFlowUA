from flask import Blueprint, request, jsonify
from app.models import db, User
from loguru import logger

user_bp = Blueprint('user', __name__, url_prefix='/api/users')


@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        logger.info(f"Отримано дані користувача з Telegram: {data}")

        telegram_id = data.get('telegram_id')
        if not telegram_id:
            return jsonify({'error': 'telegram_id is required'}), 400

        user = User.query.filter_by(telegram_id=telegram_id).first()
        if user:
            logger.info(f"Користувач з telegram_id={telegram_id} вже існує.")
        else:
            user = User(
                telegram_id=telegram_id,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                phone_number=data.get('phone_number'),
                email=data.get('email')
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Користувача збережено: {user}")

        return jsonify({'message': 'OK', 'user_id': user.id})

    except Exception as e:
        logger.exception("Помилка при збереженні користувача")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/list', methods=['GET'])
def list_users():
    try:
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'telegram_id': user.telegram_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'email': user.email
            })

        logger.info(f"Повернуто список користувачів: {len(user_list)} записів")
        return jsonify({'users': user_list})

    except Exception as e:
        logger.exception("Помилка при отриманні списку користувачів")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': f'Користувача з id={user_id} не знайдено'}), 404

            user_data = {
                'id': user.id,
                'telegram_id': user.telegram_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'email': user.email
            }

            logger.info(f"Повернуто користувача з id={user_id}")
            return jsonify(user_data)

        except Exception as e:
            logger.exception(f"Помилка при отриманні користувача з id={user_id}")
            return jsonify({'error': str(e)}), 500


@user_bp.route('/by-phone', methods=['GET'])
def get_user_by_phone():
    try:
        phone_number = request.args.get('phone_number')
        if not phone_number:
            return jsonify({'error': 'Не вказано номер телефону'}), 400

        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            logger.warning(f"Користувача з номером {phone_number} не знайдено.")
            return jsonify({'error': 'Користувача не знайдено'}), 404

        user_data = {
            'id': user.id,
            'telegram_id': user.telegram_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'email': user.email
        }

        logger.info(f"Повернуто користувача за номером телефону {phone_number}")
        return jsonify(user_data), 200

    except Exception as e:
        logger.exception("Помилка при отриманні користувача за номером телефону")
        return jsonify({'error': str(e)}), 500



@user_bp.route('/update', methods=['PUT'])
def update_user_by_phone():
    try:
        phone_number = request.args.get('phone_number')
        if not phone_number:
            return jsonify({'error': 'Не вказано номер телефону'}), 400

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Не передано даних для оновлення'}), 400

        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            logger.warning(f"Користувача з номером {phone_number} не знайдено для оновлення.")
            return jsonify({'error': 'Користувача не знайдено'}), 404

        # Оновлення полів (лише тих, що передані)
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(user, field, data[field])

        db.session.commit()
        logger.info(f"Користувача з номером {phone_number} успішно оновлено")
        return jsonify({'message': 'Користувача оновлено успішно'}), 200

    except Exception as e:
        logger.exception("Помилка при оновленні користувача")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/delete', methods=['DELETE'])
def delete_user_by_phone():
    try:
        phone_number = request.args.get('phone_number')
        if not phone_number:
            return jsonify({'error': 'Не вказано номер телефону'}), 400

        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            logger.warning(f"Користувача з номером {phone_number} не знайдено для видалення.")
            return jsonify({'error': 'Користувача не знайдено'}), 404

        db.session.delete(user)
        db.session.commit()
        logger.info(f"Користувача з номером {phone_number} успішно видалено")
        return jsonify({'message': 'Користувача видалено успішно'}), 200

    except Exception as e:
        logger.exception("Помилка при видаленні користувача")
        return jsonify({'error': str(e)}), 500



