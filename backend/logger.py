import logging

logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")

formatter = logging.Formatter(
    "{levelname} :: {asctime} :: {message}",
    style="{",
    datefmt="%d-%m-%Y %H:%M",
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.WARNING)

logger.addHandler(console_handler)
logger.addHandler(file_handler)