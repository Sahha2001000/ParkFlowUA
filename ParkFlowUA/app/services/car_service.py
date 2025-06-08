from app.models.car import db, Car
from app.models.user import User

def add_car(data):
    car = Car(**data)
    db.session.add(car)
    db.session.commit()
    return car

def get_user_cars(user_id):
    return Car.query.filter_by(user_id=user_id).all()

def delete_car(car_id):
    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return True
    return False

def update_car(car_id, data):
    car = Car.query.get(car_id)
    if not car:
        return None
    for key, value in data.items():
        setattr(car, key, value)
    db.session.commit()
    return car

def get_cars_by_phone(phone_number):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return None
    return Car.query.filter_by(user_id=user.id).all()
