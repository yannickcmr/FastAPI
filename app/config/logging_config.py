""" Default Logging Config """
import logging

def create_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)
