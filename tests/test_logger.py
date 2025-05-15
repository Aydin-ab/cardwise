import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler, SMTPHandler
from unittest import mock

import pytest

from cardwise.bank_parser.logger import LOG_FORMAT, init_logger, set_log_level, set_smtp_handler


@pytest.fixture
def logger():
    """Provides a fresh logger instance for each test by resetting the logging module."""
    return init_logger("test_logger")


def _remove_log_files():
    """Helper function to delete all possible log files created during testing."""
    log_files = ["test_logger.log", f"errors_{datetime.now().strftime('%Y-%m-%d')}.log"]

    for file in log_files:
        if os.path.exists(file):
            os.remove(file)


def test_logger_initialization(logger: logging.Logger):
    """Tests if the logger initializes correctly with default settings."""
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
    assert logger.level == logging.WARNING  # Default level
    assert len(logger.handlers) == 1  # Only console handler
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert logger.handlers[0].formatter._fmt == LOG_FORMAT  # type: ignore # Check log format


def test_set_log_level_with_verbosity(logger: logging.Logger):
    """Tests setting log level using verbosity flags (-v, -vv, -vvv)."""
    set_log_level(logger, verbosity=1)
    assert logger.level == logging.INFO

    set_log_level(logger, verbosity=2)
    assert logger.level == logging.DEBUG

    set_log_level(logger, verbosity=0)
    assert logger.level == logging.WARNING  # Back to default


def test_set_log_level_manually(logger: logging.Logger):
    """Tests setting log level explicitly using --log-level."""
    set_log_level(logger, manual_level="ERROR")
    assert logger.level == logging.ERROR
    # Check if file handlers were added
    file_handlers = [h for h in logger.handlers if isinstance(h, RotatingFileHandler)]
    assert len(file_handlers) == 2  # General log + error log
    assert file_handlers[0].level == logging.ERROR
    assert file_handlers[1].level == logging.ERROR

    set_log_level(logger, manual_level="DEBUG")
    assert logger.level == logging.DEBUG
    # Check if file handlers were added
    file_handlers = [h for h in logger.handlers if isinstance(h, RotatingFileHandler)]
    assert len(file_handlers) == 2  # General log + error log
    assert file_handlers[0].level == logging.DEBUG
    assert file_handlers[1].level == logging.ERROR

    with pytest.raises(ValueError, match="Invalid log level: INVALID"):
        set_log_level(logger, manual_level="INVALID")
    assert logger.level == logging.DEBUG  # Should not change
    assert len(logger.handlers) == 3  # No new handlers added (error log + general log + console)


def test_set_log_level_priority(logger: logging.Logger):
    """Tests that manual log level takes priority over verbosity flags."""
    set_log_level(logger, verbosity=1, manual_level="ERROR")
    assert logger.level == logging.ERROR
    file_handlers = [h for h in logger.handlers if isinstance(h, RotatingFileHandler)]
    assert len(file_handlers) == 2  # General log + error log
    assert file_handlers[0].level == logging.ERROR
    assert file_handlers[1].level == logging.ERROR  # Error log should not change when verbosity

    set_log_level(logger, verbosity=2, manual_level="WARNING")
    assert logger.level == logging.WARNING
    file_handlers = [h for h in logger.handlers if isinstance(h, RotatingFileHandler)]
    assert len(file_handlers) == 2  # General log + error log
    assert file_handlers[0].level == logging.WARNING
    assert file_handlers[1].level == logging.ERROR  # Error log should not change when verbosity

    set_log_level(logger, verbosity=1, manual_level="DEBUG")
    assert logger.level == logging.DEBUG
    file_handlers = [h for h in logger.handlers if isinstance(h, RotatingFileHandler)]
    assert len(file_handlers) == 2  # General log + error log
    assert file_handlers[0].level == logging.DEBUG
    assert file_handlers[1].level == logging.ERROR  # Error log should not change when verbosity


def test_smtp_logging_enabled(logger: logging.Logger):
    """Tests if SMTP logging is enabled when valid SMTP credentials are provided."""
    with (
        mock.patch("cardwise.bank_parser.logger.load_dotenv"),
        mock.patch.dict(
            os.environ,
            {
                "SMTP_HOST": "smtp.example.com",
                "SMTP_PORT": "587",
                "SMTP_USER": "user@example.com",
                "SMTP_PASSWORD": "password",
                "SMTP_TO": "to@example.com",
                "SMTP_FROM": "from@example.com",
            },
        ),
    ):
        set_smtp_handler(logger)
    smtp_handlers = [h for h in logger.handlers if isinstance(h, SMTPHandler)]
    assert len(smtp_handlers) == 1
    assert smtp_handlers[0].level == logging.CRITICAL
    assert smtp_handlers[0].formatter._fmt == LOG_FORMAT  # type: ignore # Check log format
    assert smtp_handlers[0].mailhost == "smtp.example.com"
    assert smtp_handlers[0].mailport == 587
    assert smtp_handlers[0].username == "user@example.com"
    assert smtp_handlers[0].password == "password"  # noqa: S105
    assert smtp_handlers[0].toaddrs == ["to@example.com"]
    assert smtp_handlers[0].fromaddr == "from@example.com"
    assert smtp_handlers[0].subject == "🚨 Cardwise Error Alert!"
    assert smtp_handlers[0].secure == ()


def test_smtp_logging_not_enabled_when_env_missing(logger: logging.Logger):
    """Tests that SMTP logging is NOT enabled when SMTP environment variables are missing."""
    with mock.patch("cardwise.bank_parser.logger.load_dotenv"), mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="SMTP environment variables are missing or incomplete"):
            set_smtp_handler(logger)

        smtp_handlers = [h for h in logger.handlers if isinstance(h, SMTPHandler)]
        assert len(smtp_handlers) == 0  # No SMTP handler should be added

    # Again with incomplete SMTP environment variables
    with (
        mock.patch("cardwise.bank_parser.logger.load_dotenv"),
        mock.patch.dict(os.environ, {"SMTP_HOST": "smtp.example.com", "SMTP_PORT": "587", "SMTP_USER": ""}),
    ):
        with pytest.raises(ValueError, match="SMTP environment variables are missing or incomplete"):
            set_smtp_handler(logger)

        smtp_handlers = [h for h in logger.handlers if isinstance(h, SMTPHandler)]
        assert len(smtp_handlers) == 0


def test_smtp_logging_updated(logger: logging.Logger):
    """Tests that SMTP logging is updated when calling set_smtp_handler multiple times."""
    with (
        mock.patch("cardwise.bank_parser.logger.load_dotenv"),
        mock.patch.dict(
            os.environ,
            {
                "SMTP_HOST": "smtp.example.com_V1",
                "SMTP_PORT": "587",
                "SMTP_USER": "user@example.com_V1",
                "SMTP_PASSWORD": "password_V1",
                "SMTP_TO": "to@example.com_V1",
                "SMTP_FROM": "from@example.com_V1",
            },
        ),
    ):
        set_smtp_handler(logger)

    with (
        mock.patch("cardwise.bank_parser.logger.load_dotenv"),
        mock.patch.dict(
            os.environ,
            {
                "SMTP_HOST": "smtp.example.com_V2",
                "SMTP_PORT": "587",
                "SMTP_USER": "user@example.com_V2",
                "SMTP_PASSWORD": "password_V2",
                "SMTP_TO": "to@example.com_V2",
                "SMTP_FROM": "from@example.com_V2",
            },
        ),
    ):
        set_smtp_handler(logger)
    smtp_handlers = [h for h in logger.handlers if isinstance(h, SMTPHandler)]
    assert len(smtp_handlers) == 1  # Only one SMTP handler should be here, no duplicates
    assert smtp_handlers[0].level == logging.CRITICAL
    assert smtp_handlers[0].formatter._fmt == LOG_FORMAT  # type: ignore # Check log format
    assert smtp_handlers[0].mailhost == "smtp.example.com_V2"
    assert smtp_handlers[0].mailport == 587
    assert smtp_handlers[0].username == "user@example.com_V2"
    assert smtp_handlers[0].password == "password_V2"  # noqa: S105
    assert smtp_handlers[0].toaddrs == ["to@example.com_V2"]
    assert smtp_handlers[0].fromaddr == "from@example.com_V2"
    assert smtp_handlers[0].subject == "🚨 Cardwise Error Alert!"
    assert smtp_handlers[0].secure == ()


def test_duplicate_handlers_prevented(logger: logging.Logger):
    """Tests that duplicate handlers are NOT added when calling set_log_level multiple times."""
    set_log_level(logger, manual_level="INFO")
    set_log_level(logger, manual_level="DEBUG")  # Should not add duplicates

    handlers = logger.handlers
    file_handlers = [h for h in handlers if isinstance(h, RotatingFileHandler)]
    console_handlers: list[logging.Handler] = [
        h for h in handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler)
    ]

    assert len(file_handlers) == 2  # General log + error log (No duplicates)
    assert len(console_handlers) == 1  # Console handler (No duplicates)

    # Add SMTP handler twice
    with (
        mock.patch("cardwise.bank_parser.logger.load_dotenv"),
        mock.patch.dict(
            os.environ,
            {
                "SMTP_HOST": "smtp.example.com_V2",
                "SMTP_PORT": "587",
                "SMTP_USER": "user@example.com_V2",
                "SMTP_PASSWORD": "password_V2",
                "SMTP_TO": "to@example.com_V2",
                "SMTP_FROM": "from@example.com_V2",
            },
        ),
    ):
        set_smtp_handler(logger)
        set_smtp_handler(logger)
    handlers = logger.handlers
    smtp_handlers = [h for h in handlers if isinstance(h, SMTPHandler)]
    assert len(smtp_handlers) == 1  # SMTP handler (if configured)


def test_logging_output_for_different_levels(caplog: pytest.LogCaptureFixture, logger: logging.Logger):
    """Tests that log messages are captured correctly for different log levels."""
    try:
        # Only warnings/errors are logged by default
        with caplog.at_level(logging.WARNING):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

        log_messages = [record.message for record in caplog.records]
        assert "Debug message" not in log_messages
        assert "Info message" not in log_messages
        assert "Warning message" in log_messages
        assert "Error message" in log_messages

        # Different log level
        set_log_level(logger, manual_level="DEBUG")

        with caplog.at_level(logging.DEBUG):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")

        log_messages = [record.message for record in caplog.records]
        assert "Debug message" in log_messages
        assert "Info message" in log_messages
        assert "Warning message" in log_messages
        assert "Error message" in log_messages
        assert "Critical message" in log_messages
    finally:
        _remove_log_files()


def test_error_file_logging_creates_log_file(logger: logging.Logger):
    """Tests that error logs create a timestamped log file."""
    try:
        set_log_level(logger, manual_level="ERROR")
        error_log_filename = f"errors_{datetime.now().strftime('%Y-%m-%d')}.log"
        assert not os.path.exists(error_log_filename)  # Should not exist before the first error log
        # Trigger an error log
        logger.error("This is a test error log.")
        assert os.path.exists(error_log_filename)
    finally:
        _remove_log_files()


def test_log_file_created_only_when_logging_enabled(logger: logging.Logger):
    """Tests that log files are only created when logging is explicitly enabled."""
    try:
        set_log_level(logger, manual_level="INFO")
        log_file_path = "test_logger.log"
        assert not os.path.exists(log_file_path)  # Should not exist before the first log
        # Trigger a log
        logger.info("This is a test log.")
        assert os.path.exists(log_file_path)  # Should exist after setting log level
    finally:
        _remove_log_files()


def test_init_logger():
    """Tests that init_logger correctly initializes a singleton logger."""
    logger = init_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "cardwise"
    assert logger.level == logging.WARNING
    assert len(logger.handlers) == 1  # Only console handler initially

    # Ensure that the logger is a singleton
    new_logger = init_logger()
    assert logger is new_logger
    assert len(logger.handlers) == 1  # No duplicate handlers added
    assert logger.name == new_logger.name
    assert logger.level == new_logger.level
    assert logger.handlers == new_logger.handlers
