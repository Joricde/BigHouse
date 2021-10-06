import os

from bighouse import logger

RES_DIR = r'./res/'
LOGS = r'./logs/'


def get_path(path, *paths):
    global RES_DIR, LOGS
    # path = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(path)
    logger.debug(root)
    RES_DIR = os.path.expanduser(RES_DIR)
    LOGS = os.path.expanduser(LOGS)
    full_path = os.path.abspath(os.path.join(path, *paths))
    if not full_path.startswith(os.path.abspath(path)):
        raise ValueError('Cannot access outside RESOURCE_DIR')
    logger.info('full_path:' + full_path)
    return os.path.join(path, *paths)
