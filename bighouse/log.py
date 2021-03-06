'''
Provide logger object.
Any other modules in "bighouse" should use "logger" from this module to log messages.
'''

import os
import sys
import logging

_error_log_file = os.path.expanduser('~/.bighouse/error.log')
_critical_log_file = os.path.expanduser('~/.bighouse/critical.log')

formatter = logging.Formatter('[%(asctime)s %(filename)s %(levelname)s: %(message)s')
logger = logging.getLogger('bighouse')
default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(formatter)
error_handler = logging.FileHandler(_error_log_file, encoding='utf8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
critical_handler = logging.FileHandler(_critical_log_file, encoding='utf8')
critical_handler.setLevel(logging.CRITICAL)
critical_handler.setFormatter(formatter)
logger.addHandler(default_handler)
logger.addHandler(error_handler)
logger.addHandler(critical_handler)
