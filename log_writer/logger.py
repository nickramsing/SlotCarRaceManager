##IMPORTS
import logging
import json
import os
import inspect
from datetime import datetime
from pathlib import Path
try:
    import yaml
except ImportError:
    raise ImportError("PyYAML is required for log_writer. PyYAML can be instead with `pip' or uv: 'pyyaml'")


class JsonLogFormatter(logging.Formatter):
    '''
    Class for formatting app logs
    '''
    def __init__(self, datetime_format: str):
        self.datetime_format = datetime_format

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now().strftime(self.datetime_format),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        return json.dumps(log_record)


def _load_config(config_path: Path) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_logger(name: str) -> logging.Logger:
    """
    Use Factory model to instantiate a configured JSON logger.
    Usage:
        logger = get_logger(__name__)
        logger.info("Hello world")
    """

    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "log_config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Logging config not found at {config_path}")

    config = _load_config(config_path)

    log_level = getattr(logging, config.get("log_level", "INFO").upper(), logging.INFO)
    log_file = config.get("log_file", "logs/app.log")
    datetime_format = config.get("datetime_format", "%Y-%m-%d %H:%M:%S")

    log_path = Path(log_file)
    if not log_path.is_absolute():
        log_path = (base_dir.parent / log_path).resolve()

    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    if not logger.handlers:
        try:
            file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to open log file: {log_path}") from e

        formatter = JsonLogFormatter(datetime_format)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
