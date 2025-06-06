from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models import db, Card, User
from app.schemas.card_schema import card_schema, cards_schema
from app.utils.logger import logger

card_bp = Blueprint("card_bp", __name__, url_prefix="/api/cards")

# 📥 Додати картку по телефону
@card_bp.route("/phone/<string:phone_number>", methods=["POST"])
def create_card(phone_number):
    data = request.get_json()
    logger.info(f"[API] Додавання картки: phone={phone_number}, data={data}")

    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        logger.warning(f"[API] Користувача з номером {phone_number} не знайдено")
        return jsonify({"message": "Користувача не знайдено"}), 404

    existing = Card.query.filter_by(user_id=user.id, number=data.get("number")).first()
    if existing:
        logger.warning("[API] Картка вже існує")
        return jsonify({"message": "Картка вже існує"}), 200

    new_card = Card(
        user_id=user.id,
        number=data.get("number"),
        exp_date=data.get("exp_date"),
        cvv=data.get("cvv")
    )

    try:
        db.session.add(new_card)
        db.session.commit()
        logger.success(f"[API] Картка додана для user_id={user.id}")
        return jsonify(card_schema.dump(new_card)), 201
    except IntegrityError:
        db.session.rollback()
        logger.exception("[API] Помилка при додаванні картки")
        return jsonify({"message": "Помилка збереження картки"}), 400


# 📄 Отримати список карток за номером телефону
@card_bp.route("/phone/<string:phone_number>", methods=["GET"])
def get_cards_by_phone(phone_number):
    logger.info(f"[API] Отримання карток для телефону: {phone_number}")

    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404

    cards = Card.query.filter_by(user_id=user.id).all()
    return jsonify(cards_schema.dump(cards)), 200


# ❌ Видалити картку за телефоном і номером картки
@card_bp.route("/phone/<string:phone_number>/<string:card_number>", methods=["DELETE"])
def delete_card_by_number(phone_number, card_number):
    logger.info(f"[API] Видалення картки {card_number} для телефону {phone_number}")

    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404

    card = Card.query.filter_by(user_id=user.id, number=card_number).first()
    if not card:
        return jsonify({"message": "Картку не знайдено"}), 404

    db.session.delete(card)
    db.session.commit()
    logger.success(f"[API] Картку {card_number} видалено для user_id={user.id}")
    return jsonify({"message": "Картку видалено"}), 200

@card_bp.route("/<int:card_id>", methods=["DELETE"])
def delete_card_by_id(card_id):
    card = Card.query.get(card_id)
    if not card:
        return jsonify({"message": "Картку не знайдено"}), 404

    db.session.delete(card)
    db.session.commit()
    return jsonify({"message": "Картку видалено"}), 200
