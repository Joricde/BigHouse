import io
import os
import random
import threading
import time
import zipfile
from bighouse import logger, res
from conf import ConfigClass

# path_a = '..\\logs\\part_a\\'
path_a = res.get_path(res.LOGS, 'part_a')
# path_b = '..\\logs\\part_b\\'
path_b = res.get_path(res.LOGS, 'part_b')

work_path = path_a
list_coin = ['BTC/BUSD', 'DOGE/BUSD', 'ETH/BUSD', 'ADA/BUSD']


def getExchangeData():
    global work_path, path_a, path_b, list_coin
    exchange = ConfigClass.CustomBinanceData()
    db_test = ConfigClass.CustomMysql()
    cursor = db_test.cursor()
    timestamp = 0
    price = 0
    default_path = os.path.dirname(os.path.dirname(__file__))  # default path is main entrance path
    logger.info('default_path' + default_path)

    now_time = time.strftime("%Y-%m-%d", time.localtime())

    for coin in list_coin:
        coin_name = str(coin).split('/')
        coin_name = coin_name[0] + coin_name[1]
        sql_sentence = f"""
            create table if not exists {coin_name}(
                time_stamp timestamp,
                price float
            )
        """
        cursor.execute(sql_sentence)
        if not os.path.exists(os.path.join(path_a, coin_name)):
            os.makedirs(os.path.join(path_a, coin_name))
        if not os.path.exists(os.path.join(path_b, coin_name)):
            os.makedirs(os.path.join(path_b, coin_name))

    while True:
        try:
            for coin in list_coin:
                coin_name = str(coin).split('/')
                coin_name = coin_name[0] + coin_name[1]
                file_path = os.path.join(work_path, coin_name, now_time + coin_name + '.log')
                # file_path = f'{work_path}{coin_name}/{now_time}{coin_name}.log'
                with open(file_path, "a+", buffering=io.DEFAULT_BUFFER_SIZE) as coin_data:
                    response = exchange.fetch_ticker(coin)
                    coin_data.write(str(response))
                    coin_data.write('\n')
                    timestamp = response["timestamp"]
                    now_time = time.strftime("%Y-%m-%d", time.localtime(int(timestamp / 1000)))
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp / 1000)))
                    price = response["bid"]
                    query = f"""
                        insert into {coin_name}(time_stamp, price) values (%s, %s)
                    """
                    values = (timestamp, price)
                    cursor.execute(query, values)
                    coin_data.close()
            db_test.commit()
            logger.debug(price)
        except Exception as e:
            logger.error(e)
            db_test.rollback()
        time.sleep(30)


def compress():
    global work_path, path_a, path_b
    comp_cycle = time.localtime().tm_mday
    comp_month = time.localtime().tm_mon % 12 + 1
    logger.info(f'comp_cycle:, {comp_cycle}')
    while True:
        # logger.debug(time.localtime().tm_mday % 30 == comp_cycle - 1)
        # if time.localtime().tm_mday % 30 == comp_cycle:  # debug
        if time.localtime().tm_mday % 30 == comp_cycle and time.localtime().tm_mon == comp_month:
            logger.info(f'compress month: {comp_month}')
            comp_month = comp_month % 12 + 1
            compress_part = work_path
            work_path = path_b if work_path == path_a else path_a
            t = time.strftime("%Y-%m-%d", time.localtime())
            with zipfile.ZipFile(f'{res.get_path(res.LOGS)}{t}-{random.randint(1, 1000)}.zip', 'w',
                                 compression=zipfile.ZIP_DEFLATED,
                                 compresslevel=9) as target:
                for root, dirs, files in os.walk(compress_part):
                    logger.debug('root' + root)
                    for f in files:
                        logger.debug(os.path.join(root, f))
                        target.write(os.path.join(root, f))
                target.close()
            for root, dirs, files in os.walk(compress_part):
                for f in files:
                    logger.debug(os.path.join(root, f))
                    os.remove(os.path.join(root, f))
            # compress_part = path_b if work_path == path_a else path_a
        time.sleep(360)


def start():
    thread_1 = threading.Thread(target=getExchangeData)
    thread_2 = threading.Thread(target=compress)
    thread_1.start()
    thread_2.start()
    thread_1.join()
