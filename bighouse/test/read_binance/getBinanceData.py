import io
import os
import time
import sys
from bighouse import logger
from conf import ConfigClass

sys.path.append('..\..\BigHouse')

exchange = ConfigClass.CustomBinanceData()

db_test = ConfigClass.CustomMysql()
cursor = db_test.cursor()
# print(exchange.custom_fetch_balance())

i = 1
timestamp = 0
price = 0
list_coin = ['BTC/BUSD', 'DOGE/BUSD', 'ETH/BUSD', 'ADA/BUSD']
default_path = os.path.dirname(os.path.dirname(__file__))  # default path is main entrance path
logger.info(default_path)

now_time = time.strftime("%Y-%m-%d", time.localtime())
coin_root_path = '../logs/'

for res in list_coin:
    coin_name = str(res).split('/')
    coin_name = coin_name[0] + coin_name[1]
    sql_sentence = f"""
        create table if not exists {coin_name}(
            time_stamp timestamp,
            price float
        )
    """
    cursor.execute(sql_sentence)
    coin_dirs = coin_root_path + coin_name
    if not os.path.exists(coin_dirs):
        os.makedirs(coin_dirs)

while True:
    try:
        for res in list_coin:
            coin_name = str(res).split('/')
            coin_name = coin_name[0] + coin_name[1]
            file_path = f'{coin_root_path}{coin_name}/{now_time}{coin_name}.log'
            with open(file_path, "a+", buffering=io.DEFAULT_BUFFER_SIZE) as coin_data:
                response = exchange.fetch_ticker(res)
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

    except Exception as e:
        logger.error(e)
        db_test.rollback()
    logger.info(price)
    time.sleep(10)
