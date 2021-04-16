import logging, sys
from logging.handlers import TimedRotatingFileHandler
#FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "debug.log"


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    blue = "\x1b[1;34m"
    yellow = "\x1b[1;33m"
    red = "\x1b[31;21m"
    green = "\x1b[1;36m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(name)s : %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(CustomFormatter())
    return file_handler


def get_logger(logger_name, level):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level) # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger