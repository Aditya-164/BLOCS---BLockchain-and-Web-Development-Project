import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("decentralized_storage")
    return logger
