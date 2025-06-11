import logging
from typing import Optional


def set_log_level(logger: logging.Logger, manual_level: Optional[str] = None, verbosity: int = 0):
    """
    Adjusts logging based on manual log level or verbosity.

    **Behavior**:
    - If `manual_level` is provided, set the logger level to it.
    - If `manual_level` is None and `verbosity` is 0, remove all handlers except the console.
    - If `manual_level` is None and `verbosity` > 0, set the logger level based on verbosity.

    **Usage Options**:
    - `manual_level`: Manually set level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
    - `verbosity`: Adjusts logging level (`-v` for INFO, `-vv` for DEBUG).
    """
    if manual_level:
        # Set the logger level to the manual level
        valid_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
        level = manual_level.upper()
        if level not in valid_levels:
            raise ValueError(f"Invalid log level: {manual_level} (Use one of {valid_levels})")
        logger.setLevel(level)
    elif verbosity == 0:
        # Remove all handlers except the console
        for handler in logger.handlers[:]:
            if not isinstance(handler, logging.StreamHandler):
                logger.removeHandler(handler)
        logger.setLevel(logging.WARNING)
    else:
        # Set the logger level based on verbosity
        if verbosity == 1:
            logger.setLevel(logging.INFO)
        elif verbosity >= 2:
            logger.setLevel(logging.DEBUG)
