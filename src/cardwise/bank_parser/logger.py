import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler, SMTPHandler
from typing import Optional, Union

from dotenv import load_dotenv

# ANSI Colors for Terminal Logging
RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[94m",  # Blue
    "INFO": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "CRITICAL": "\033[95m",  # Magenta
}

# Log format
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_DATE = datetime.now().strftime("%Y-%m-%d")


# 🎨 Custom formatter for colored console output
class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_color = COLORS.get(record.levelname, RESET)
        log_message = super().format(record)
        return f"{log_color}{log_message}{RESET}"


def _create_file_handler(name: str, log_level: Union[str, int]) -> RotatingFileHandler:
    """Creates a rotating file handler for general logs."""
    file_handler = RotatingFileHandler(name, maxBytes=5_000_000, backupCount=3, delay=True)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    file_handler.setLevel(log_level)
    return file_handler


def _create_error_handler() -> RotatingFileHandler:
    """Creates a rotating file handler for error logs."""
    error_handler = RotatingFileHandler(f"errors_{LOG_DATE}.log", maxBytes=2_000_000, backupCount=2, delay=True)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    error_handler.setLevel(logging.ERROR)
    return error_handler


def _enable_file_logging(logger: logging.Logger):
    """Enables file logging when an explicit log level is set."""
    if not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        logger.addHandler(_create_file_handler(f"{logger.name}.log", logger.level))
        logger.addHandler(_create_error_handler())
    else:
        # Update the log level of the file handler of filename 'logger.name'
        for handler in logger.handlers:
            if isinstance(handler, RotatingFileHandler) and f"{logger.name}.log" in handler.baseFilename:
                handler.setLevel(logger.level)
                break


def _create_smtp_handler() -> SMTPHandler:
    """Creates an SMTP handler if email credentials are provided."""
    load_dotenv()

    SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
    SMTP_PORT = os.getenv("SMTP_PORT", "").strip()
    SMTP_USER = os.getenv("SMTP_USER", "").strip()
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()
    SMTP_TO = os.getenv("SMTP_TO", "").strip()
    SMTP_FROM = os.getenv("SMTP_FROM", "").strip()

    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_TO, SMTP_FROM]):
        raise ValueError("SMTP environment variables are missing or incomplete")

    smtp_handler = SMTPHandler(
        mailhost=(SMTP_HOST, int(SMTP_PORT)),
        fromaddr=SMTP_FROM,
        toaddrs=[SMTP_TO],
        subject="🚨 Cardwise Error Alert!",
        credentials=(SMTP_USER, SMTP_PASSWORD),
        secure=(),
    )
    smtp_handler.setLevel(logging.CRITICAL)
    smtp_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return smtp_handler


def set_smtp_handler(logger: logging.Logger):
    """Adds an SMTP handler for critical error logging."""
    # Check if SMTP handler doesn't already exist
    if any(isinstance(h, SMTPHandler) for h in logger.handlers):
        # Remove existing SMTP handler
        for handler in logger.handlers:
            if isinstance(handler, SMTPHandler):
                logger.removeHandler(handler)
                break
    # Add new SMTP handler
    smtp_handler = _create_smtp_handler()
    logger.addHandler(smtp_handler)


def _set_log_level_manually(logger: logging.Logger, manual_level: str):
    """Sets the log level manually."""
    valid_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    level = manual_level.upper()
    if level not in valid_levels:
        raise ValueError(f"Invalid log level: {manual_level} (Use one of {valid_levels})")
    logger.setLevel(level)
    _enable_file_logging(logger)


def _set_log_level_with_verbosity(logger: logging.Logger, verbosity: int):
    """Sets the log level based on verbosity."""
    if verbosity == 0:
        logger.setLevel(logging.WARNING)
    elif verbosity == 1:
        logger.setLevel(logging.INFO)
    elif verbosity >= 2:
        logger.setLevel(logging.DEBUG)


def set_log_level(logger: logging.Logger, verbosity: int = 0, manual_level: Optional[str] = None):
    """
    Adjusts logging based on verbosity (`-v`) or manual log level (`--log-level`).

    **Usage Options:**
    - `-v`: Logs INFO messages.
    - `-vv`: Logs DEBUG messages.
    - `--log-level <level>`: Manually set level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

    ✅ Log files will **only** be created if `--log-level` is used.
    """
    if manual_level:
        _set_log_level_manually(logger, manual_level)
    else:
        _set_log_level_with_verbosity(logger, verbosity)


def init_logger(name: str = "cardwise", default_level: Union[str, int] = logging.WARNING) -> logging.Logger:
    """Initializes and returns a logger instance with default settings."""
    _reset_logging()
    logger = logging.getLogger(name)

    logger.setLevel(default_level)  # Default level

    # Console Handler (Colored)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(LOG_FORMAT))
    logger.addHandler(console_handler)

    return logger


# Delete logger if exists
def _reset_logging():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    loggers.append(logging.getLogger())
    for logger in loggers:
        handlers = logger.handlers[:]
        for handler in handlers:
            logger.removeHandler(handler)
            handler.close()
        logger.setLevel(logging.NOTSET)
        logger.propagate = True
