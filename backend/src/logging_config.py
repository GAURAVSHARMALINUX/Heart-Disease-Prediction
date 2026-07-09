import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    LOG_FILE = "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3),
        ]
    )

    return logging.getLogger("heart-disease-api")
