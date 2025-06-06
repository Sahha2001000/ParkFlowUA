from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models import db, Car, User
from app.schemas.cars_schema import car_schema, cars_schema
from app.utils.logger import logger
from app.utils.plate_utils import normalize_license_plate

car_bp = Blueprint('car_bp', __name__, url_prefix='/api/cars')

# 1. Додати авто
@car_bp.route('/<int:user_id>', methods=['POST'])
def add_car(user_id):
    data = request.json
    logger.info(f"[API] Запит на додавання авто для user_id={user_id}, data={data}")

    # Нормалізація держномера
    normalized_plate = normalize_license_plate(data.get('license_plate', ''))
    data['license_plate'] = normalized_plate

    new_car = Car(
        user_id=user_id,
        brand=data.get('brand'),
        model=data.get('model'),
        year=data.get('year'),
        license_plate=normalized_plate
    )

    try:
        db.session.add(new_car)
        db.session.commit()
        logger.success(f"[API] Авто додано: {new_car}")
        return jsonify(car_schema.dump(new_car)), 201

    except IntegrityError:
        db.session.rollback()
        existing_car = Car.query.filter_by(license_plate=normalized_plate).first()
        logger.warning(f"[API] Авто з номером {normalized_plate} вже існує: {existing_car}")
        return jsonify({
            "message": "Авто з таким номером вже існує",
            "existing_car": car_schema.dump(existing_car)
        }), 200

# 2. Список авто за user_id
@car_bp.route('/user/<int:user_id>', methods=['GET'])
def get_cars_by_user(user_id):
    cars = Car.query.filter_by(user_id=user_id).all()
    return jsonify(cars_schema.dump(cars)), 200

# 3. Список авто за номером телефону
@car_bp.route('/phone/<string:phone_number>', methods=['GET'])
def get_cars_by_phone(phone_number):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"message": "Користувача з таким номером не знайдено"}), 404
    cars = Car.query.filter_by(user_id=user.id).all()
    return jsonify(cars_schema.dump(cars)), 200

# 4. Список авто за держ. номером (license_plate)
@car_bp.route('/plate/<string:license_plate>', methods=['GET'])
def get_car_by_plate(license_plate):
    normalized_plate = normalize_license_plate(license_plate)
    car = Car.query.filter_by(license_plate=normalized_plate).first()
    if not car:
        return jsonify({"message": "Авто з таким номером не знайдено"}), 404
    return jsonify(car_schema.dump(car)), 200

# 5. Оновити авто за id
@car_bp.route('/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    data = request.json
    new_plate = normalize_license_plate(data.get('license_plate')) if data.get('license_plate') else car.license_plate

    car.brand = data.get('brand', car.brand)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    car.license_plate = new_plate
    try:
        db.session.commit()
        return jsonify(car_schema.dump(car)), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Такий номер вже існує"}), 409

# 6. Видалити авто за id
@car_bp.route('/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": f"Авто з ID {car_id} видалено"}), 200

# Додати авто за номером телефону
@car_bp.route('/phone/<string:phone_number>', methods=['POST'])
def add_car_by_phone(phone_number):
    data = request.json
    logger.info(f"[API] Запит на додавання авто за номером телефону: {phone_number}, data={data}")

    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        logger.warning(f"[API] Користувача з телефоном {phone_number} не знайдено")
        return jsonify({"message": "Користувача з таким номером телефону не знайдено"}), 404

    normalized_plate = normalize_license_plate(data.get('license_plate'))
    existing = Car.query.filter_by(license_plate=normalized_plate).first()
    if existing:
        logger.warning(f"[API] Авто з номером {normalized_plate} вже існує")
        return jsonify({"message": "Авто з таким номером вже додано"}), 200

    new_car = Car(
        user_id=user.id,
        brand=data.get('brand'),
        model=data.get('model'),
        year=data.get('year'),
        license_plate=normalized_plate
    )
    db.session.add(new_car)
    db.session.commit()
    logger.success(f"[API] Авто додано: {new_car}")
    return jsonify(car_schema.dump(new_car)), 201

# Оновити авто за номером телефону та держ. номером
@car_bp.route('/phone/<string:phone_number>/<string:license_plate>', methods=['PUT'])
def update_car_by_plate(phone_number, license_plate):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404

    normalized_plate = normalize_license_plate(license_plate)
    car = Car.query.filter_by(user_id=user.id, license_plate=normalized_plate).first()
    if not car:
        return jsonify({"message": "Авто не знайдено"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Дані не надано"}), 400

    car.brand = data.get('brand', car.brand)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    db.session.commit()

    return jsonify({"message": "Інформацію про авто оновлено"}), 200


@car_bp.route('/phone/<string:phone_number>/<string:license_plate>', methods=['DELETE'])
def delete_car_by_plate(phone_number, license_plate):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        logger.warning(f"[DELETE] Користувача не знайдено: {phone_number}")
        return jsonify({"message": "Користувача не знайдено"}), 404

    normalized_plate = normalize_license_plate(license_plate)
    logger.info(f"[DELETE] Спроба видалення авто: {normalized_plate} для user_id={user.id}")

    car = Car.query.filter_by(user_id=user.id, license_plate=normalized_plate).first()
    if not car:
        logger.warning(f"[DELETE] Авто не знайдено: {normalized_plate} для user_id={user.id}")
        return jsonify({"message": "Авто не знайдено"}), 404

    db.session.delete(car)
    db.session.commit()
    logger.success(f"[DELETE] Авто видалено: {normalized_plate} для user_id={user.id}")
    return '', 204
