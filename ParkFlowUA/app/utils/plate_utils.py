from loguru import logger

def normalize_license_plate(plate: str) -> str:
    """
    Перетворює номерний знак у стандартизований формат (латиниця + верхній регістр),
    замінює кирилицю на відповідні латинські символи.
    """
    if not plate:
        logger.warning("[PLATE] Порожній номер авто для нормалізації")
        return ""

    original = plate
    plate = (
        plate.upper()
        .replace("І", "I")
        .replace("Ї", "Y")
        .replace("Є", "E")
        .replace("А", "A")
        .replace("В", "B")
        .replace("Е", "E")
        .replace("К", "K")
        .replace("М", "M")
        .replace("Н", "H")
        .replace("О", "O")
        .replace("Р", "P")
        .replace("С", "C")
        .replace("Т", "T")
        .replace("У", "Y")
        .replace("Х", "X")
        .replace("З", "Z")
    )

    logger.info(f"[PLATE] Нормалізація номера: '{original}' → '{plate}'")
    return plate
