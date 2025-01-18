import logging
import os

class Logger:
    @staticmethod
    def get_logger():
        logger = logging.getLogger("AppLogger")
        if not logger.handlers:
            handler = logging.FileHandler("src/logs/app.log")
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger