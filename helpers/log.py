import logging


class Log:
    levels = {
        'error': logging.ERROR,
        'trace': logging.INFO,
        'debug': logging.DEBUG,
        'notset': logging.NOTSET,
    }

    def __init__(self, level='notset'):
        self.log_level = self.levels.get(level, logging.NOTSET)
        # Each emulator owns its logger; normal runs never open a trace file.
        self.logger = logging.Logger('minips', self.log_level)
        self.logger.propagate = False
        self.logger.disabled = self.log_level == logging.NOTSET
        self.handler = (logging.NullHandler() if self.logger.disabled else
                        logging.FileHandler('./minips.trace', mode='w'))
        self.handler.setLevel(self.log_level)
        self.logger.addHandler(self.handler)

    def close(self):
        self.handler.close()

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def trace(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)
