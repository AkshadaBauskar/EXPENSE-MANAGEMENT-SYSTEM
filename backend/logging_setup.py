import logging
import os

def setup_logger(name, log_file='server.log', level=logging.DEBUG):
    # Define the correct path for the log file
    log_dir = 'backend'
    log_file = os.path.join(log_dir, log_file)

    # Ensure the directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a custom logger
    logger = logging.getLogger(name)

    # Configure the logger
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
