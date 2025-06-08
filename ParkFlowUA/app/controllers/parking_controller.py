from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.services.parking_service import (
    create_city, create_parking, create_spot,
    update_city, update_parking, update_spot,
    delete_city, delete_parking, delete_spot,
    get_all_cities, get_all_parkings, get_all_spots,
    get_available_spots, get_spot_by_id
)
from app.schemas.parking_schemas import CitySchema, ParkingSchema, SpotSchema
from app.utils.logger import logger

parking_bp = Blueprint('parking_bp', __name__, url_prefix='/api/parking')

city_schema = CitySchema()
parking_schema = ParkingSchema()
spot_schema = SpotSchema()
city_schemas = CitySchema(many=True)
parking_schemas = ParkingSchema(many=True)
spot_schemas = SpotSchema(many=True)

# ====== CITY ======

@parking_bp.route('/city', methods=['POST'])
def add_city():
    data = request.json
    logger.info(f"[API] Додавання міста: {data}")
    try:
        city = create_city(data['name'])
        return jsonify(city_schema.dump(city)), 201
    except IntegrityError:
        logger.warning(f"[API] Місто '{data['name']}' вже існує")
        return jsonify({"message": f"Місто '{data['name']}' вже існує"}), 200

@parking_bp.route('/city/<int:city_id>', methods=['PUT'])
def edit_city(city_id):
    data = request.json
    logger.info(f"[API] Оновлення міста ID={city_id}: {data}")
    city = update_city(city_id, data['name'])
    return jsonify(city_schema.dump(city)), 200

@parking_bp.route('/city/<int:city_id>', methods=['DELETE'])
def remove_city(city_id):
    logger.info(f"[API] Видалення міста ID={city_id}")
    delete_city(city_id)
    return jsonify({'message': 'Місто видалено'}), 204

@parking_bp.route('/cities', methods=['GET'])
def list_cities():
    logger.info("[API] Отримання списку міст")
    cities = get_all_cities()
    return jsonify(city_schemas.dump(cities)), 200

# ====== PARKING ======

@parking_bp.route('/parking', methods=['POST'])
def add_parking():
    data = request.json
    logger.info(f"[API] Додавання паркінгу: {data}")
    try:
        parking = create_parking(data['name'], data['city_id'])
        return jsonify(parking_schema.dump(parking)), 201
    except IntegrityError:
        logger.warning(f"[API] Паркінг '{data['name']}' вже існує")
        return jsonify({"message": f"Паркінг '{data['name']}' вже існує"}), 200

@parking_bp.route('/parking/<int:parking_id>', methods=['PUT'])
def edit_parking(parking_id):
    data = request.json
    logger.info(f"[API] Оновлення паркінгу ID={parking_id}: {data}")
    parking = update_parking(parking_id, data['name'], data['city_id'])
    return jsonify(parking_schema.dump(parking)), 200

@parking_bp.route('/parking/<int:parking_id>', methods=['DELETE'])
def remove_parking(parking_id):
    logger.info(f"[API] Видалення паркінгу ID={parking_id}")
    delete_parking(parking_id)
    return jsonify({'message': 'Паркінг видалено'}), 204

@parking_bp.route('/parkings', methods=['GET'])
def list_parkings():
    logger.info("[API] Отримання списку паркінгів")
    parkings = get_all_parkings()
    return jsonify(parking_schemas.dump(parkings)), 200

# ====== SPOT ======

@parking_bp.route('/spot', methods=['POST'])
def add_spot():
    data = request.json
    logger.info(f"[API] Додавання паркомісця: {data}")
    try:
        spot = create_spot(
            data['number'],
            data['parking_id'],
            data.get('hourly_rate', 50.0)
        )
        return jsonify(spot_schema.dump(spot)), 201
    except IntegrityError:
        logger.warning(f"[API] Паркомісце '{data['number']}' вже існує")
        return jsonify({"message": f"Паркомісце '{data['number']}' вже існує"}), 200

@parking_bp.route('/spot/<int:spot_id>', methods=['PUT'])
def edit_spot(spot_id):
    data = request.json
    logger.info(f"[API] Оновлення паркомісця ID={spot_id}: {data}")
    spot = update_spot(
        spot_id=spot_id,
        number=data['number'],
        parking_id=data['parking_id'],
        is_available=data.get('is_available', True),
        occupied_from=data.get('occupied_from'),
        occupied_to=data.get('occupied_to')
    )
    return jsonify(spot_schema.dump(spot)), 200

@parking_bp.route('/spot/<int:spot_id>', methods=['DELETE'])
def remove_spot(spot_id):
    logger.info(f"[API] Видалення паркомісця ID={spot_id}")
    delete_spot(spot_id)
    return jsonify({'message': 'Паркомісце видалено'}), 204

@parking_bp.route('/spots', methods=['GET'])
def list_spots():
    logger.info("[API] Отримання всіх паркомісць")
    spots = get_all_spots()
    return jsonify(spot_schemas.dump(spots)), 200

@parking_bp.route('/spots/available', methods=['GET'])
def list_available_spots():
    parking_id = request.args.get('parking_id')
    logger.info(f"[API] Отримання вільних паркомісць для паркінгу ID={parking_id}")
    spots = get_available_spots(parking_id)
    return jsonify(spot_schemas.dump(spots)), 200

@parking_bp.route('/spot/<int:spot_id>', methods=['GET'])
def get_spot_by_id_api(spot_id):
    spot = get_spot_by_id(spot_id)
    if spot:
        return jsonify({
            "id": spot.id,
            "number": spot.number,
            "parking_id": spot.parking_id,
            "is_available": spot.is_available,
            "hourly_rate": spot.hourly_rate,
            "occupied_from": spot.occupied_from,
            "occupied_until": spot.occupied_until
        }), 200
    else:
        return jsonify({"error": f"Паркомісце з ID={spot_id} не знайдено"}), 404
