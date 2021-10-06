### 
```bat  
pip install ccxt
pip install pymysql
pip install -U requests[socks]
```
### example
```python  

import json
import asyncio
from config import ConfigClass

loop = asyncio.get_event_loop()
exchange = ConfigClass.CustomBinanceData()


class JustUsingExample(object):
    """
    The Unified CCXT API
    """
    test_exchange = ConfigClass.CustomBinanceData()

    def fetchMarkets(self, params={}):
        """从交易所提取所有有效市场的清单，返回市场对象数组。
        有些交易所没有办法通过其在线API获取市场清单，
        CCXT采用硬编码的方式返回这些交易所的市场清单。
     """
        return self.test_exchange.fetch_markets()

    def fetchStatus(self):
        """
        返回交易所状态信息，可能使用API或者硬编码实现
        :return:
        """
        return self.test_exchange.fetch_status()

    def fetchOrderBook(self, symbol, limit=None, params={}):
        """
        该请求将返回symbol交易对的交易所当前可用的买价和卖价订单。
        :param symbol: string
        :param limit: int
        Default 100; max 5000. Valid limits:[5, 10, 20, 50, 100, 500, 1000, 5000]
            number of queries
        :param params: etc...
        :return:
        """
        return self.test_exchange.fetch_order_book("ETC/BUSD", 100)

    def fetchL2OrderBook(self, symbol, limit=None, params={}):
        """
        与fetchOrderBook()参数相同
        """
        return self.test_exchange.fetch_l2_order_book("ETC/BUSD", 100)

    def fetchTicker(self, symbol):
        """
        获取指定交易符号的最新行情数据
        :param symbol:
        :return:
        """
        return self.test_exchange.fetch_ticker("BTC/BUSD")

    def fetchBalance(self):
        """
        查询账号余额
        :return:
        """
        return self.test_exchange.fetch_balance()

    def createOrder(self, symbol, type, side, amount, price=None, params={}):
        """
        创建订单 type: 'market' 时不需要 price,
        :param symbol:
        :param type:
        :param side:
        :param amount:
        :param price:
        :param params:
        :return:
        """
        return self.test_exchange.create_order('DOGE/BUSD', 'limit', 'buy', 10000, 0.4)

    def cancelOrder(self, id, symbol, params={}):
        """
        取消订单， 需要orderId，和该id对应的symbol， creatOrder时会返回createId，
        :param id:
        :param symbol:
        :param params:
        :return:
        """
        return self.test_exchange.cancel_order(217093211, 'DOGE/BUSD')

    def fetchOrders(self, id, symbol, params={}):
        """
        查询订单，需要orderId，和该id对应的symbol（撤单似乎无法查询撤销的委托/订单
        :param id:
        :param symbol:
        :param params:
        :return:
        """
        return self.test_exchange.fetch_orders('DOGE/BUSD')

    def fetchOpenOrders(self, symbol, since=None, limit=None, params={}):
        """
        不知道是什么概念，暂时不涉及
        since时间戳，减少无用订单集
        """
        pass

    def fetchClosedOrders(self, symbol, since=None, limit=None, params={}):
        """
        symbol = undefined, since = undefined, limit = undefined, params = {}
        不知道是什么概念，暂时不涉及
        """
        pass

    def fetchMyTrades(self, symbol, since=None, limit=None, params={}):
        """
        不知道什么概念，暂不涉及
        """
        pass


"""
    fetchMarkets()：
        从交易所提取所有有效市场的清单，返回市场对象数组。有些 交易所没有办法通过其在线API获取市场清单，CCXT采用硬编码的方式返回这些交易所的市场清单。
    loadMarkets([reload])：
        返回对象形式的市场清单并在交易所实例上缓存，键为交易符号。如果 之前已经载入过，则从缓存中返回结果，除非是强制使用了reload标志并设置为true。
    fetchOrderBook(symbol[, limit = undefined[, params = {}]])：
        获取指定市场交易符号的L2/L3委托账本
    fetchStatus([, params = {}])：
        返回交易所状态信息，可能使用API或者硬编码实现
    fetchL2OrderBook(symbol[, limit = undefined[, params]])：
        获取交易符号的2层（价格聚合）委托账本
    fetchTrades(symbol[, since[, [limit, [params]]]])：
        获取指定交易符号的最近交易
    fetchTicker(symbol)：
        获取指定交易符号的最新行情数据
    fetchBalance():
        获取余额数据, 返回太多未持有的币种信息，采用custom_fetch_balance代替
    createOrder(symbol, type, side, amount[, price[, params]])
        创建订单 type: 'market' 时不需要 price,
    createLimitBuyOrder(symbol, amount, price[, params]):
        limit的方式创建买入（币）订单 不采用
    createLimitSellOrder(symbol, amount, price[, params])
        limit的方式创建卖出（币）订单 不采用
    createMarketBuyOrder(symbol, amount[, params])
        market的方式创建卖出（币）订单 不采用
    createMarketSellOrder(symbol, amount[, params])
        market的方式创建卖出（币）订单 不采用
    cancelOrder(id[, symbol[, params]])
        取消订单
    fetchOrder(id[, symbol[, params]])
        查找订单，提供id，精准查询，日期过长可能无法查询？
    fetchOrders([symbol[, since[, limit[, params]]]])
        按symbol查找订单，量过多时采用分页接收
    fetchOpenOrders([symbol[, since, limit, params]]]])
    fetchClosedOrders([symbol[, since[, limit[, params]]]])
    fetchMyTrades([symbol[, since[, limit[, params]]]])

"""

```
### run()
