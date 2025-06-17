import logging.config
from pathlib import Path

import yaml

from ingestion.core.config import settings


def setup_logging():
    log_config_path = Path(__file__).resolve().parent / "logging_config.yaml"
    with open(log_config_path, "r") as f:
        config = yaml.safe_load(f)

    level = settings.log_level.upper()
    config["loggers"]["ingestion"]["level"] = level

    logging.config.dictConfig(config)
