import logging

class Logger:
    def __init__(self):
        log_file_path = "./logs/LOGGER.log"
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)