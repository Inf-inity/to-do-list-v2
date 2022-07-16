import logging
import sys

from uvicorn.config import LOGGING_CONFIG
from uvicorn.logging import DefaultFormatter

from .environment import LOG_LEVEL


fmt = "[%(asctime)s] %(levelprefix)s %(message)s"
logging_formatter = DefaultFormatter(fmt, use_colors=True)
LOGGING_CONFIG["formatters"]["default"]["fmt"] = fmt
LOGGING_CONFIG["formatters"]["default"]["use_colors"] = True
LOGGING_CONFIG["formatters"]["access"][
    "fmt"
] = '[%(asctime)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'

logging_handler = logging.StreamHandler(sys.stdout)
logging_handler.setFormatter(logging_formatter)


def get_logger(name: str) -> logging.Logger:

    logger: logging.Logger = logging.getLogger(name)
    logger.addHandler(logging_handler)
    logger.setLevel(LOG_LEVEL.upper())

    return logger
