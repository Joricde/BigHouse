import asyncio
import math
import time

from retrying import retry

from bighouse.src.core import model
import conf.ConfigClass
from bighouse import logger


class TransactionCurrency(object):
    _exchange = dict()
    _symbol = None
    commodity_coin_name = 0
    principal_coin_name = None

    commodity_coin_unit = None
    price_unit = None

    timestamp = None

    order_status = None
    wallet_free_principal = None
    wallet_free_commodity = None

    price_now = None
    buy_point = None
    sell_point = None
    reference_point = None
    reduce_point = None
    increase_point = None

    orderId = None

    def __init__(self, symbol):
        """
        :param symbol: such as 'ETH/BUSD'
        """

        try:
            loop = asyncio.get_event_loop()
            self.commodity_coin_name = str(symbol).split('/')[0]
            self.principal_coin_name = str(symbol).split('/')[1]
            self.__exchange = conf.ConfigClass.CustomBinanceData()
            self.__symbol = symbol
            loop.run_until_complete(loop.create_task(self.fetch_balance()))
            loop.run_until_complete(loop.create_task(self.GetTickerPrice()))
        except SystemExit:
            logger.error(SystemExit)
            raise SystemExit
        for unit in range(20):
            if self.price_now * 10 ** unit > 100:
                self.price_unit = unit + 2
                self.commodity_coin_unit = 4 - unit
                break
        logger.info(f"init TransactionCurrency of {self.__symbol} successful")

    async def fetch_balance(self) -> dict:
        """
         Refresh self wallet attribute
        :return: response
        """
        try:
            response = self.__exchange.fetch_balance()
        except TypeError as e:
            logger.error(e.args)
            raise e
        for index in response['info']['balances']:
            if index['asset'] == self.commodity_coin_name:
                self.wallet_free_commodity = float(index['free'])
                logger.debug(self.wallet_free_commodity, "1")
            elif index['asset'] == self.principal_coin_name:
                self.wallet_free_principal = float(index['free'])
        logger.info("fetch balance  \n",
                    f"{self.commodity_coin_name}: {self.wallet_free_commodity}\n"
                    f"{self.principal_coin_name}: {self.wallet_free_principal}", "finish")
        return response

    async def GetTickerPrice(self, ) -> float:
        """
        refresh self price_now
        :return:a float price
        """
        response = None
        try:
            response = self.__exchange.fetch_ticker(self.__symbol)
            # response = self._exchange.fapiPublicGetTickerPrice(
            #     {'symbol': f'{self.commodity_coin_name}{self.principal_coin_name}'})
            self.price_now = float(response['bid'])
            self.timestamp = response['timestamp']
        except TypeError as e:
            logger.error(e.args)
            raise e
        logger.info("get the last price successful now price is ", f"{self.price_now}")
        return float(response['bid'])

    async def create_buy_order(self, price=None):
        """
        refresh the feed back
        :return: response
        """
        price = self.price_now if price is None else price
        buy_coin_number = math.floor(
            self.wallet_free_principal / self.price_now *
            10 ** self.commodity_coin_unit) / 10 ** self.commodity_coin_unit
        try:
            response = self.__exchange.create_order(f'{self.__symbol}', 'limit', 'buy', buy_coin_number, price)
        except TypeError as e:
            logger.error(e.args)
            raise e
        logger.info(f"buy response: {response}")
        self.orderId = response['info']['orderId']
        self.timestamp = response['timestamp']
        self.order_status = response['status']
        logger.info('creat buy order successful  ', f'order id: {self.orderId}, '
                                                    f'timestamp: {self.timestamp}'
                                                    f'status: {self.order_status}')
        return response

    async def create_sell_order(self, price=None) -> list:
        price = self.price_now if price is None else price
        price = math.floor(price * 10 ** self.price_unit) / 10 ** self.price_unit
        sell_coin_number = math.floor(
            self.wallet_free_commodity * 10 ** self.commodity_coin_unit) / 10 ** self.commodity_coin_unit
        try:
            response = self.__exchange.create_order(
                f'{self.__symbol}', 'limit', 'sell', sell_coin_number, price)
        except TypeError as e:
            logger.error(e.args)
            raise e
        logger.info(f"sell response: {response}")
        self.timestamp = response['timestamp']
        self.order_status = response['status']
        logger.info('creat sell order successful  ', f'order id: {self.orderId},'
                                                     f' timestamp: {self.timestamp}'
                                                     f'status : {self.order_status}')
        return response

    async def cancelOrder(self):
        try:
            response = self.__exchange.cancel_order(self.orderId, self.__symbol)
        except TypeError as e:
            logger.error(e.args)
            raise e
        self.timestamp = response['timestamp']
        self.order_status = response['status']
        logger.info('had cancel order successful  ', f'order id: {self.orderId},'
                                                     f' timestamp: {self.timestamp}'
                                                     f'status : {self.order_status}')
        return response

    @retry(stop_max_attempt_number=5)
    def auto_rich(self, transaction_model=False):
        operation = order = sell = False
        loop = asyncio.get_event_loop()
        while True:
            time.sleep(60)
            price_query = loop.create_task(self.GetTickerPrice())
            loop.run_until_complete(price_query)
            self.price_now = price_query.result()

            if not operation and self.wallet_free_principal > 10:  # try to order
                order = model.ModelImpl.order(self.price_now)
                if order:
                    loop.create_task(self.create_buy_order())
                continue
            elif operation:  # try to sell
                # loop.run_until_complete(loop.create_task(self.fetch_balance()))
                sell = model.ModelImpl.sell(self.price_now)
                if sell:
                    loop.create_task(self.create_sell_order())


test_t = TransactionCurrency('BNB/BUSD')
test_t.auto_rich()
