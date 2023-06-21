import logging
import datetime

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
_user = ''

def _setup_logger():
    log_filename = now.strftime("%Y-%m-%d") + '-' + _user + '.log'
    file_handler = logging.FileHandler(log_filename, mode='a')
    file_handler.setFormatter(logging.Formatter(datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(file_handler)

def log_start(user):
    global _user
    _user = user        
    _setup_logger()
    start_line = f"===== {timestamp} | START | USER: {_user} ====="
    logger.info(start_line)

def log_end():
    end_line = f"===== {timestamp} | END | USER: {_user} ====="
    logger.info(end_line)

def log_info(message):
    logger.info(message)

def log_error(error_message):
    error_line = f"===== {timestamp} | ERROR | USER: {_user} ====="
    logger.error(error_line)
    logger.error(error_message)
