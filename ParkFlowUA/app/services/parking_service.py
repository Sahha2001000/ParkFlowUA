from app.models.parking import db, City, Parking, Spot
from app.utils.logger import logger
from datetime import datetime

# ===================== CITY =====================

def create_city(name):
    city = City(name=name)
    db.session.add(city)
    db.session.commit()
    logger.success(f"[Service] Створено місто: {city}")
    return city

def update_city(city_id, new_name):
    city = City.query.get_or_404(city_id)
    logger.info(f"[Service] Оновлення міста ID={city_id}: '{city.name}' → '{new_name}'")
    city.name = new_name
    db.session.commit()
    return city

def delete_city(city_id):
    city = City.query.get_or_404(city_id)
    logger.warning(f"[Service] Видалення міста: {city}")
    db.session.delete(city)
    db.session.commit()

def get_all_cities():
    cities = City.query.all()
    logger.debug(f"[Service] Отримано список міст: {len(cities)} шт.")
    return cities

# ===================== PARKING =====================

def create_parking(name, city_id):
    parking = Parking(name=name, city_id=city_id)
    db.session.add(parking)
    db.session.commit()
    logger.success(f"[Service] Створено паркінг: {parking}")
    return parking

def update_parking(parking_id, name, city_id):
    parking = Parking.query.get_or_404(parking_id)
    logger.info(f"[Service] Оновлення паркінгу ID={parking_id}")
    parking.name = name
    parking.city_id = city_id
    db.session.commit()
    return parking

def delete_parking(parking_id):
    parking = Parking.query.get_or_404(parking_id)
    logger.warning(f"[Service] Видалення паркінгу: {parking}")
    db.session.delete(parking)
    db.session.commit()

def get_all_parkings():
    return Parking.query.all()

# ===================== SPOT =====================

def create_spot(number, parking_id, hourly_rate=50.0):
    spot = Spot(number=number, parking_id=parking_id, hourly_rate=hourly_rate)
    db.session.add(spot)
    db.session.commit()
    logger.success(f"[Service] Створено паркомісце: {spot}")
    return spot

def update_spot(spot_id, number, parking_id, is_available=True, occupied_from=None, occupied_to=None):
    spot = Spot.query.get_or_404(spot_id)
    spot.number = number
    spot.parking_id = parking_id
    spot.is_available = is_available
    spot.occupied_from = occupied_from
    spot.occupied_to = occupied_to
    db.session.commit()
    logger.info(f"[Service] Оновлено паркомісце ID={spot_id}")
    return spot

def delete_spot(spot_id):
    spot = Spot.query.get_or_404(spot_id)
    db.session.delete(spot)
    db.session.commit()
    logger.warning(f"[Service] Видалено паркомісце: {spot}")

def get_all_spots():
    return Spot.query.all()

def get_available_spots(parking_id=None):
    query = Spot.query.filter_by(is_available=True)
    if parking_id:
        query = query.filter_by(parking_id=parking_id)
    return query.all()

def get_spot_by_id(spot_id: int):
    spot = Spot.query.get(spot_id)
    if spot:
        logger.debug(f"[Service] Отримано паркомісце ID={spot_id}")
    return spot
