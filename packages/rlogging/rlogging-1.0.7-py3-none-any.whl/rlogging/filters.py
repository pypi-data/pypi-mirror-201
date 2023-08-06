import logging


class RsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return True


class WarningFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno > logging.WARNING
