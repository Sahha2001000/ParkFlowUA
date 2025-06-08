from kafka.admin import KafkaAdminClient, NewTopic
from loguru import logger
from app.config import Config

KAFKA_BOOTSTRAP_SERVERS = Config.KAFKA_BOOTSTRAP_SERVERS
KAFKA_TOPIC_NAME = Config.KAFKA_TOPIC

logger.add("logs/kafka_topic_creation.log", rotation="500 KB", level="INFO")

def create_kafka_topic():
    logger.info(f"Починаємо створення топіка '{KAFKA_TOPIC_NAME}'")
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        client_id='topic_creator'
    )

    topic = NewTopic(
        name=KAFKA_TOPIC_NAME,
        num_partitions=1,
        replication_factor=1
    )

    try:
        admin_client.create_topics([topic])
        logger.info(f"Топік '{KAFKA_TOPIC_NAME}' успішно створено")
    except Exception as e:
        logger.warning(f"Не вдалося створити топік '{KAFKA_TOPIC_NAME}': {e}")

if __name__ == "__main__":
    create_kafka_topic()
