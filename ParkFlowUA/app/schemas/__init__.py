from flask_marshmallow import Marshmallow
from app.utils.logger import logger

# Ініціалізація глобального об'єкта Marshmallow
ma = Marshmallow()

logger.info("Ініціалізовано Marshmallow-схеми")
