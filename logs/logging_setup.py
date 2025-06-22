import os
import logging

def setup_logger(file_name):
    log_dir = "logs/files"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file_path = os.path.join(log_dir, f"{file_name}.log")

    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file_path, mode='w')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger