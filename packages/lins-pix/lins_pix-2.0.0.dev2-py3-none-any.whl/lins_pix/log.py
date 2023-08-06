import graypy
import logging

from datetime import datetime
from lins_pix.settings import (
    LOG_ENV,
    GRAYLOG_HOST,
    GRAYLOG_PORT
)


class LogFilter(logging.Filter):
    def filter(self, record):
        record.settings = LOG_ENV
        record.application = "lins_pix"
        return True

class Log:
    class __Log:
        def __init__(self):
            self.logger = logging.getLogger("python-graylog-logger")
            host = GRAYLOG_HOST
            port = int(GRAYLOG_PORT) if GRAYLOG_PORT else None

            self.logger.setLevel(logging.INFO)
            handler = graypy.GELFUDPHandler(host, port, level_names=True)
            self.logger.addHandler(handler)
            self.logger.addFilter(LogFilter())

    instance = None
    def __getattr__(self, name):
        return getattr(self.instance, name)

    @classmethod
    def error(cls, message):
        if not Log.instance:
            Log.instance = Log.__Log()
        cls.instance.logger.error(message)
        print('Erro: {}'.format(message))

    @classmethod
    def info(cls, message):
        if not Log.instance:
            Log.instance = Log.__Log()
        cls.instance.logger.info(message)
        print('Info: {}'.format(message))
