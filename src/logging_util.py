import logging


class Logger:
    def __init__(self, logging_keyword):
        self.logging_keyword = logging_keyword

    def debug(self, msg: str):
        logging.debug(f"{self.logging_keyword}: {msg}")

    def info(self, msg: str):
        logging.info(f"{self.logging_keyword}: {msg}")

    def warning(self, msg: str):
        logging.warning(f"{self.logging_keyword}: {msg}")

    def error(self, msg: str):
        logging.error(f"{self.logging_keyword}: {msg}")
