import logging.config
import os
from pathlib import Path

import yaml


def init_app() -> None:
    log_dir = Path(".logs")
    log_dir.mkdir(exist_ok=True)

    config_path = Path("config/logging.yaml")
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as f:
            logging.config.dictConfig(yaml.safe_load(f.read()))
    else:
        logging.basicConfig(level=logging.INFO)
