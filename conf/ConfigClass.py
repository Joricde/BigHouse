"""
当且仅当在次文件定义配置文件
"""
import json
import os

from ccxt import binance
from pymysql import connect


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


def get_config_path() -> str:
    path = os.path.dirname(__file__)
    path = os.path.join(path, "config.json")

    return path


@Singleton
class CustomBinanceData(binance):
    """
    默认采用此子类代替直接使用ccxt的binance类
    默认各方法中的参数采用一下形式输入
    *symbol: string
        'ETH/BUSD', etc。。。
    *type：string(enum)
        'limit' or 'market',
    *side: string(enum)
        'buy' or 'sell',
    *amount: number
        该币的数量 coin number
    *price : number
        该币单位价格unit price
    *:params: 自定义内容，根据具体交易所的接口编写
    """

    def __init__(self):
        try:
            with open(get_config_path()) as config_read:
                class_config_read = json.load(config_read)
                if class_config_read['class_config']['enableRateLimit'] == 'True':
                    class_config_read['class_config']['enableRateLimit'] = True
                else:
                    class_config_read['class_config']['enableRateLimit'] = False
                config_read.close()
            super(CustomBinanceData, self).__init__(class_config_read['class_config'])
        except Exception:
            raise Exception

        print("UserBinanceData init success")

    def custom_fetch_balance(self, params=None):
        """
        获取当前账号余额，
        仅返回余额不为零的币种的余额
        :param 需要查询的币
        :return: 当前余额
        """
        if params is None:
            params = {}
            all_balance = super(CustomBinanceData, self).fetch_balance()
            all_balance = all_balance['info']
            custom_need_balance = {}
            tem = []
            for key in all_balance:
                if key != 'balances':
                    custom_need_balance[key] = all_balance[key]
                else:
                    for son_key in all_balance['balances']:
                        if float(son_key['free']) > 1.0e-6 or float(son_key['locked']) > 1.0e-6:
                            tem.append(son_key)

                    custom_need_balance['balances'] = tem
            return custom_need_balance
        else:
            return super(CustomBinanceData, self).fetch_balance(params)

    def custom_create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        创造订单
        :param symbol: 交易币的类型如 ETC/BUSD （string
        :param type: limit、market 限价单 （string
        :param side: 行为 sell、buy （string
        :param amount: 数量 需要买入的币种数量 （number
        :param price: 为卖的币开价 （number
        :param params: 条件等
        :return: {
            'info': order,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol.txt': symbol.txt,
            'type': type,
            'timeInForce': timeInForce,
            'postOnly': postOnly,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'amount': amount,
            'cost': cost,
            'average': None,
            'filled': filled,
            'remaining': None,
            'status': status,
            'fee': None,
            'trades': trades,
        }
        """
        if params is None:
            params = {}
        super().create_order(self, symbol, type, side, amount, price, params)

    """此处开始，为调用币安原生接口方法，采用隐式函数的形式实例化前生成，，放在此次仅是提示有该函数存在"""

    def fapiPublicGetTickerPrice(self, params=None):
        """
        :param params:  {'symbol': 'BTCUSDT'}
        :return:
        """
        pass

    def v3GetTickerPrice(self, param):
        """
        当fapiPublicGetTickerPrice选用的备用节点
        :param param:
        :return:
        """
        pass


@Singleton
class CustomMysql(connect):

    def __init__(self):
        try:
            with open(get_config_path()) as config_read:
                mysql_config = json.load(config_read)
                super(CustomMysql, self).__init__(
                    host=mysql_config["mysql"]["host"],
                    password=mysql_config["mysql"]["password"],
                    user=mysql_config["mysql"]["user"],
                    database=mysql_config["mysql"]["database"],
                    charset=mysql_config["mysql"]["charset"])
                config_read.close()
        except Exception:
            raise Exception
        print("UserMysql init success")
