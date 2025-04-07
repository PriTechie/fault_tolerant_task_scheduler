import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str, log_file: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger  # Avoid duplicate handlers if already set

    file_handler = logging.FileHandler(os.path.join(LOG_DIR, log_file), encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

# Main scheduler logger
logger = get_logger("SchedulerLogger", "scheduler.log")

