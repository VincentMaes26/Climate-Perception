import logging
from pathlib import Path
import sys
import datetime

def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

    # Sends output to log file
    logfile_name = datetime.datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
    file_handler = logging.FileHandler(r"..\scripts\logfiles\{}.log".format(logfile_name))
    file_handler.setFormatter(formatter)

    # Sends output to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger