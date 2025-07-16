# logging_config.py

import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Use DEBUG if you want more verbose logs
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
        # Optional: write logs to a file
        # filename="app.log", filemode="w"
    )
