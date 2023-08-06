import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s: %(levelname)s:%(name)s:%(message)s")

file_handler = RotatingFileHandler(
    filename="ask_robot.log",
    maxBytes=50 * 1024 * 1024,
    backupCount=500,
    encoding="utf-8",
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
