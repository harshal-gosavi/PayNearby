import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent
log_file = os.path.join(BASE_DIR, f'logs/server.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_file_log = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=10)  # LOG file is 10 MB
rotating_file_log.setLevel(logging.DEBUG)
rotating_file_log.setFormatter(formatter)
root_logger.addHandler(rotating_file_log)
