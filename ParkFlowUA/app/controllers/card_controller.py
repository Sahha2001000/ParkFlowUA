from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.services.card_service import (
    create_card_service,
    get_cards_by_phone_service,
    delete_card_by_number_service,
    delete_card_by_id_service,
    update_card_by_id_service
)
from app.utils.logger import logger

card_bp = Blueprint("card_bp", __name__, url_prefix="/api/cards")


@card_bp.route("/phone/<string:phone_number>", methods=["POST"])
def create_card(phone_number):
    data = request.get_json()
    logger.info(f"[API] POST /cards/phone/{phone_number} | Data: {data}")
    return create_card_service(phone_number, data)


@card_bp.route("/phone/<string:phone_number>", methods=["GET"])
def get_cards_by_phone(phone_number):
    logger.info(f"[API] GET /cards/phone/{phone_number}")
    return get_cards_by_phone_service(phone_number)


@card_bp.route("/phone/<string:phone_number>/<string:card_number>", methods=["DELETE"])
def delete_card_by_number(phone_number, card_number):
    logger.info(f"[API] DELETE /cards/phone/{phone_number}/{card_number}")
    return delete_card_by_number_service(phone_number, card_number)


@card_bp.route("/<int:card_id>", methods=["DELETE"])
def delete_card_by_id(card_id):
    logger.info(f"[API] DELETE /cards/{card_id}")
    return delete_card_by_id_service(card_id)


@card_bp.route("/<int:card_id>", methods=["PUT"])
def update_card(card_id):
    data = request.get_json()
    logger.info(f"[API] PUT /cards/{card_id} | Data: {data}")
    return update_card_by_id_service(card_id, data)
