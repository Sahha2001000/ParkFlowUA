from flask import jsonify
from sqlalchemy.exc import IntegrityError
from app.models import db, Card, User
from app.schemas.card_schema import card_schema, cards_schema
from app.utils.logger import logger


def create_card_service(phone_number: str, data: dict):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404

    existing = Card.query.filter_by(user_id=user.id, number=data.get("number")).first()
    if existing:
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
        return jsonify(card_schema.dump(new_card)), 201
    except IntegrityError:
        db.session.rollback()
        logger.exception("[SERVICE] Помилка при створенні картки")
        return jsonify({"message": "Помилка збереження картки"}), 400


def get_cards_by_phone_service(phone_number: str):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404

    cards = Card.query.filter_by(user_id=user.id).all()
    return jsonify(cards_schema.dump(cards)), 200


def delete_card_by_number_service(phone_number: str, card_number: str):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404

    card = Card.query.filter_by(user_id=user.id, number=card_number).first()
    if not card:
        return jsonify({"message": "Картку не знайдено"}), 404

    db.session.delete(card)
    db.session.commit()
    return jsonify({"message": "Картку видалено"}), 200


def delete_card_by_id_service(card_id: int):
    card = Card.query.get(card_id)
    if not card:
        return jsonify({"message": "Картку не знайдено"}), 404

    db.session.delete(card)
    db.session.commit()
    return jsonify({"message": "Картку видалено"}), 200


def update_card_by_id_service(card_id: int, data: dict):
    card = Card.query.get(card_id)
    if not card:
        return jsonify({"message": "Картку не знайдено"}), 404

    try:
        card.number = data.get("number", card.number)
        card.exp_date = data.get("exp_date", card.exp_date)
        card.cvv = data.get("cvv", card.cvv)
        db.session.commit()
        return jsonify(card_schema.dump(card)), 200
    except Exception as e:
        logger.exception(f"[SERVICE] Помилка при оновленні картки ID={card_id}: {e}")
        db.session.rollback()
        return jsonify({"message": "Помилка при оновленні"}), 400
