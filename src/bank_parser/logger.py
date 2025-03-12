import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler, SMTPHandler
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables safely (default to empty string if missing)
SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = os.getenv("SMTP_PORT", "").strip()
SMTP_USER = os.getenv("SMTP_USER", "").strip()
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()
SMTP_TO = os.getenv("SMTP_TO", "").strip()
SMTP_FROM = os.getenv("SMTP_FROM", "").strip()

# Get current date for timestamped error logs
log_date = datetime.now().strftime("%Y-%m-%d")
error_log_filename = f"errors_{log_date}.log"
verbose_log_filename = "verbose_cardwise.log"  # Separate verbose log

# ANSI Colors for Terminal Logging
RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[94m",  # Blue
    "INFO": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "CRITICAL": "\033[95m",  # Magenta
}


# 🖨️ Custom Formatter for Colored Console Output
class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_color = COLORS.get(record.levelname, RESET)
        log_message = super().format(record)
        return f"{log_color}{log_message}{RESET}"


# Log format
log_format = "%(asctime)s [%(levelname)s] %(message)s"

# 📁 Main log file (rotates at 5MB, keeps last 3 logs)
file_handler = RotatingFileHandler("cardwise.log", maxBytes=5_000_000, backupCount=3)
file_handler.setFormatter(logging.Formatter(log_format))
file_handler.setLevel(logging.INFO)

# 📁 Verbose log file (separate logging when `-v` is used)
verbose_file_handler = RotatingFileHandler(verbose_log_filename, maxBytes=5_000_000, backupCount=2)
verbose_file_handler.setFormatter(logging.Formatter(log_format))
verbose_file_handler.setLevel(logging.DEBUG)  # Always logs everything

# 📁 Timestamped error log file (logs only `ERROR` and `CRITICAL`)
error_handler = RotatingFileHandler(error_log_filename, maxBytes=2_000_000, backupCount=2)
error_handler.setFormatter(logging.Formatter(log_format))
error_handler.setLevel(logging.ERROR)

# 🎨 Console handler (Uses colored formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter(log_format))  # ✅ Apply colors only to console logs
console_handler.setLevel(logging.WARNING)  # Default: Only show warnings/errors

# 🔧 Create logger
logger = logging.getLogger("cardwise")
logger.setLevel(logging.WARNING)  # Default: Disabled unless `-v` is used
logger.addHandler(file_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)


# 📧 Email Error Notifications (Only if SMTP credentials are provided)
if all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_TO, SMTP_FROM]):
    try:
        smtp_handler = SMTPHandler(
            mailhost=(SMTP_HOST, int(SMTP_PORT)),
            fromaddr=SMTP_FROM,
            toaddrs=[SMTP_TO],
            subject="🚨 Cardwise Error Alert!",
            credentials=(SMTP_USER, SMTP_PASSWORD),
            secure=(),
        )
        smtp_handler.setLevel(logging.CRITICAL)  # Send emails only for critical errors
        smtp_handler.setFormatter(logging.Formatter(log_format))  # No colors for emails
        logger.addHandler(smtp_handler)
        logger.info("✅ SMTP logging enabled")
    except Exception as e:
        logger.error(f"❌ Failed to configure SMTP logging: {e}")
else:
    logger.warning("⚠️ SMTP logging disabled - Missing required environment variables")


# Suppress logs from external libraries
logging.getLogger("requests").setLevel(logging.WARNING)  # Suppress detailed logs from requests
logging.getLogger("urllib3").setLevel(logging.WARNING)  # Same for urllib3


### **🔹 Function to Control Log Level via CLI Arguments**
def set_log_level(verbosity: int = 0, manual_level: Optional[str] = None):
    """
    Adjusts logging based on verbosity (`-v`) or manual log level (`--log-level`).

    **Usage Options:**
    - `-v`: Logs INFO messages.
    - `-vv`: Logs DEBUG messages.
    - `-vvv`: Logs DEBUG + writes to `verbose_cardwise.log`.
    - `--log-level <level>`: Manually set level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
    """
    if manual_level:
        level = manual_level.upper()
        all_levels = ["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]
        if level in all_levels:
            logger.setLevel(level)
            console_handler.setLevel(level)
            logger.info(f"🔍 Manual log level set to {level}")
            return
        else:
            logger.error(f"❌ Invalid log level: {manual_level} (Use one of {all_levels})")
            return

    if verbosity == 0:
        logger.setLevel(logging.WARNING)  # Default (Only warnings and errors)
        console_handler.setLevel(logging.WARNING)
    elif verbosity == 1:
        logger.setLevel(logging.INFO)  # `-v`
        console_handler.setLevel(logging.INFO)
    elif verbosity >= 2:
        logger.setLevel(logging.DEBUG)  # `-vv` and above
        console_handler.setLevel(logging.DEBUG)

        if verbosity >= 3:
            logger.addHandler(verbose_file_handler)  # `-vvv` adds file logging

    logger.info(f"🔍 Logging level set to {logging.getLevelName(logger.level)}")
