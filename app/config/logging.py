# logging_config.py
import logging

from config.settings import settings


# Central logging configuration
def setup_logging():
    # Create a logger
    logger = logging.getLogger(settings.NICKNAME)
    logger.setLevel(logging.DEBUG)  # Set the base logging level

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Log level for console
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)

    return logger


# Create a global logger instance
logger = setup_logging()
