import logging
import os
import config

def setup_logger(name):
    """Configure le logger pour l'application."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    log_dir = os.path.join(config.OUTPUT_FOLDER, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    fh = logging.FileHandler(os.path.join(log_dir, f'{name}.log'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
