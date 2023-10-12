from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    postgres_url = os.getenv(
        "POSTGRES_URL", "postgres://admin:passwd@turbine-postgres:5432/turbine"
    )
    celery_broker_url = os.getenv("CELERY_BROKER_URL", "amqp://rabbitmq")
    celery_backend_url = os.getenv("CELERY_BACKEND_URL", "db+sqlite:///results.db")
    kafka_url = os.getenv("KAFKA_URL", "localhost:19092")
    debezium_url = os.getenv("DEBEZIUM_URL", "http://localhost:8083")
