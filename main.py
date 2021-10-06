import os
from bighouse import logger, res


def setup_environment():
    upgrade = f'pip install --upgrade pip'
    install = f'pip install -r {os.getcwd()}\\requirements.txt'
    os.system(upgrade)
    logger.info('pip upgrade finish')
    os.system(install)
    logger.info('pip install requirements.txt finish')


if __name__ == '__main__':
    # setup_environment()
    # path_b = res.get_path(res.LOGS, 'part_b')
    # logger.debug(path_b)
    from bighouse.test import read_binance
    read_binance.getBinanceData.start()
