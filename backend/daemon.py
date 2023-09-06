from src.daemon.daemon import Daemon
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
)


daemon = Daemon()
daemon.run()
