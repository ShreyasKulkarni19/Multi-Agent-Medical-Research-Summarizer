# logging_config.py

import logging

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # or logging.DEBUG

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1️⃣ Console Handler with UTF-8 encoding
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # Avoid Unicode errors in console output
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # 2️⃣ File Handler with UTF-8 encoding
    file_handler = logging.FileHandler("pipeline.log", mode="a", encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
