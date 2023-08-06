import logging
import os
from typing import Dict

from .platform import PROD

# Conventional kernel log file location. Studio will stream the log to cloudwatch.
KERNEL_LOG_FILE = "/var/log/studio/dw-ganymede-kernel.log"
METRICS_LOGGER_NAME = "metrics"

CRITICAL = logging.getLevelName(logging.CRITICAL)
ERROR = logging.getLevelName(logging.ERROR)


class _DispatchingFormatter:
    def __init__(self, formatters: Dict[str, logging.Formatter], default_formatter):
        self._formatters = formatters
        self._default_formatter = default_formatter

    def format(self, record: logging.LogRecord):
        formatter = self._formatters.get(record.name, self._default_formatter)
        return formatter.format(record)


def create_log_dir():
    try:
        studio_dir = "/var/log/studio"
        if not os.path.exists(studio_dir):
            os.mkdir(studio_dir)
    except OSError as error:
        logging.error(
            f"Error while creating logging directory {studio_dir} with Error: {error}"
        )


def setup_logging(stage=PROD):
    try:
        create_log_dir()
        # Create log formatter
        log_str_fmt = "[%(asctime)s %(levelname)s %(name)s %(thread)d] %(message)s"
        date_fmt = "%m/%d/%Y %H:%M:%S"
        log_formatter = _DispatchingFormatter(
            {
                METRICS_LOGGER_NAME: logging.Formatter("%(message)s"),
            },
            default_formatter=logging.Formatter(log_str_fmt, datefmt=date_fmt),
        )
        # Configure log handler
        log_handler = logging.handlers.TimedRotatingFileHandler(
            KERNEL_LOG_FILE, when="h", interval=3, backupCount=3
        )
        log_handler.setFormatter(log_formatter)

        # Set up default logger
        default_logger = logging.getLogger()
        default_logger.addHandler(log_handler)

        # Set up metrics logger
        metrics_logger = logging.getLogger(METRICS_LOGGER_NAME)
        # Metrics logger should not propagate to root logger again
        metrics_logger.propagate = False
        metrics_logger.addHandler(log_handler)

        if stage == PROD:
            default_logger.setLevel(logging.INFO)
            metrics_logger.setLevel(logging.INFO)
        else:
            default_logger.setLevel(logging.DEBUG)
            metrics_logger.setLevel(logging.DEBUG)
    except Exception as error:
        logging.error(f"Error while creating logging handlers with Error: {error}")


def get_metrics_logger():
    return logging.getLogger(METRICS_LOGGER_NAME)
