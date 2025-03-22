import logging


def get_logger():
    logger = logging.getLogger("ws")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s:     %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
