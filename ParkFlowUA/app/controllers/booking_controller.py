from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models import db, Booking, User, Car
from app.models.parking import Spot
from app.models.card import Card
from app.schemas.booking_schemas import booking_schema, bookings_schema
from app.utils.logger import logger

booking_bp = Blueprint("booking_bp", __name__, url_prefix="/api/bookings")


# 1. Створити бронювання за номером телефону
@booking_bp.route("/phone/<string:phone_number>", methods=["POST"])
def create_booking_by_phone(phone_number):
    data = request.json
    logger.info(f"[API] Створення бронювання: phone={phone_number}, data={data}")

    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        logger.warning(f"[API] Користувач {phone_number} не знайдений")
        return jsonify({"message": "Користувача не знайдено"}), 404

    car = Car.query.filter_by(id=data.get("car_id"), user_id=user.id).first()
    if not car:
        logger.warning(f"[API] Авто з ID={data.get('car_id')} не знайдено або не належить користувачу")
        return jsonify({"message": "Авто не знайдено або не належить користувачу"}), 404

    spot = Spot.query.get(data.get("spot_id"))
    if not spot:
        return jsonify({"message": "Місце не знайдено"}), 404

    card = Card.query.filter_by(id=data.get("card_id"), user_id=user.id).first()
    if not card:
        logger.warning(f"[API] Картка ID={data.get('card_id')} не знайдена або не належить користувачу")
        return jsonify({"message": "Картку не знайдено або не належить користувачу"}), 404

    try:
        duration_hours = float(data.get("duration_hours", 1))
        if duration_hours <= 0:
            raise ValueError()
    except Exception:
        return jsonify({"message": "Некоректна тривалість"}), 400

    total_price = round(spot.hourly_rate * duration_hours, 2)

    try:
        now = datetime.utcnow()
        occupied_from = now
        occupied_until = now + timedelta(hours=duration_hours)

        # 🟡 оновлюємо spot (паркомісце)
        spot.occupied_from = occupied_from
        spot.occupied_until = occupied_until
        spot.is_available = False

        booking = Booking(
            spot_id=spot.id,
            car_id=car.id,
            user_id=user.id,
            card_id=card.id,
            duration_hours=duration_hours,
            total_price=total_price,
            created_at=now,
            status='pending'
        )

        db.session.add(booking)
        db.session.commit()

        logger.success(f"[API] Бронювання створено: {booking}")

        # 🔁 Додаємо у відповідь також occupied_from та occupied_until
        response = booking_schema.dump(booking)
        response.update({
            "occupied_from": occupied_from.isoformat(),
            "occupied_until": occupied_until.isoformat()
        })

        return jsonify(response), 201

    except IntegrityError:
        db.session.rollback()
        logger.exception("[API] Помилка створення бронювання")
        return jsonify({"message": "Не вдалося створити бронювання"}), 400


# 2. Отримати список бронювань за номером телефону
@booking_bp.route("/phone/<string:phone_number>", methods=["GET"])
def get_bookings_by_phone(phone_number):
    logger.info(f"[API] Отримання бронювань користувача: {phone_number}")

    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404

    bookings = Booking.query.filter_by(user_id=user.id).all()
    return jsonify(bookings_schema.dump(bookings)), 200


# 3. Перевірка статусу бронювання
@booking_bp.route("/<int:booking_id>", methods=["GET"])
def get_booking_status(booking_id):
    logger.info(f"[API] Перевірка статусу бронювання ID={booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    return jsonify({
        "id": booking.id,
        "spot_id": booking.spot_id,
        "car_id": booking.car_id,
        "user_id": booking.user_id,
        "card_id": booking.card_id,
        "status": booking.status,
        "created_at": booking.created_at,
        "paid_at": booking.paid_at,
        "duration_hours": booking.duration_hours,
        "total_price": booking.total_price,
    }), 200


# 4. Видалення бронювання
@booking_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    logger.success(f"[API] Бронювання ID={booking_id} видалено")
    return jsonify({"message": f"Бронювання ID {booking_id} видалено"}), 200
