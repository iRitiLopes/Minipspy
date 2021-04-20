import logging
import sys

class Log:
    levels = {
        'error': logging.ERROR,
        'trace': logging.INFO,
        'debug': logging.DEBUG,
        'notset': logging.NOTSET
    }
    def __init__(self, level='notset') -> None:
        self.log_level = self.levels.get(level, logging.NOTSET)
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        f = open('./minips.trace', 'w')
        if self.log_level == logging.NOTSET:
            self.logger.disabled = True
        else:
            self.logger.disabled = False
        self.handler = logging.StreamHandler(f)
        self.handler.setLevel(self.log_level)
        self.logger.addHandler(self.handler)


    def error(self, message):
        self.logger.error(message)


    def warning(self, message):
        self.logger.warning(message)


    def trace(self, message):
        self.logger.info(message)


    def debug(self, message):
        self.logger.debug(message)
