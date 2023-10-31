import datetime 
import logging 
import os 

from screeninfo import get_monitors

def setup_logger(log_path, name):
    """
    Setup logger with a name for each messager

    Log saved to a single file with distinguishable names.
    """
    date = datetime.datetime.now().strftime('%Y%m%d')
    hhmmss = datetime.datetime.now().strftime('%H%M%S')
    log_filename = f'{date}_{hhmmss}.txt'
    fn = os.path.join(log_path, log_filename)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(fn)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

def get_timestamp():
    """Retrieve YYYYMMDD_HHMMSS timestamp"""
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def get_monitor():
    """Retrieve primary monitor info (includes width and height)"""
    for m in get_monitors():
        if m.is_primary:
            break 
    return m