from src.daemon.daemon import Daemon
from config import Config

print(Config.kafka_url)
daemon = Daemon(kafka_url=Config.kafka_url)
daemon.run()
