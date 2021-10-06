import os
import logging

os.makedirs(os.path.expanduser('~/.bighouse'), exist_ok=True)
from bighouse.log import logger

logger.setLevel(logging.INFO)
