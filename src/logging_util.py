import logging
from src import setting


class Logger:
    def __init__(self, logging_from: str):
        # basic logging setting
        if setting.LOGGING_FILE is None:
            logging.basicConfig(level=setting.LOGGING_LEVEL)
        else:
            logging.basicConfig(filename=setting.LOGGING_FILE,
                                filemode='w',
                                level=setting.LOGGING_LEVEL)

        # specifies which component the log is coming from
        self.logging_keyword = logging_from

    def debug(self, msg: str):
        logging.debug(f"{self.logging_keyword}: {msg}")

    def info(self, msg: str):
        logging.info(f"{self.logging_keyword}: {msg}")

    def warning(self, msg: str):
        logging.warning(f"{self.logging_keyword}: {msg}")

    def error(self, msg: str):
        logging.error(f"{self.logging_keyword}: {msg}")
