import asyncio
import math
import time

from retrying import retry


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
            self._exchange = config.ConfigClass.CustomBinanceData()
            self._symbol = symbol
            loop.run_until_complete(loop.create_task(self.fetch_balance()))
            loop.run_until_complete(loop.create_task(self.GetTickerPrice()))
            for unit in range(20):
                if self.price_now * 10 ** unit > 100:
                    self.price_unit = unit + 2
                    self.commodity_coin_unit = 4 - unit
                    break
        except Exception:
            raise Exception
        print(f"init TransactionCurrency of {self._symbol} successful")

    async def fetch_balance(self) -> dict:
        """
         Refresh self wallet attribute
        :return: response
        """
        response = self._exchange.fetch_balance()
        for index in response['info']['balances']:
            if index['asset'] == self.commodity_coin_name:
                self.wallet_free_commodity = float(index['free'])
                print(self.wallet_free_commodity, "1")
            elif index['asset'] == self.principal_coin_name:
                self.wallet_free_principal = float(index['free'])
        print("fetch balance  \n",
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
            response = self._exchange.fetch_ticker(self._symbol)
            # response = self._exchange.fapiPublicGetTickerPrice(
            #     {'symbol': f'{self.commodity_coin_name}{self.principal_coin_name}'})
            self.price_now = float(response['bid'])
            self.timestamp = response['timestamp']
            print("get the last price successful now price is ", f"{self.price_now}")
        except TypeError as e:
            print(e.args)
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
        response = self._exchange.create_order(f'{self._symbol}', 'limit', 'buy', buy_coin_number, price)
        print(f"buy response: {response}")
        self.orderId = response['info']['orderId']
        self.timestamp = response['timestamp']
        self.order_status = response['status']
        print('creat buy order successful  ', f'order id: {self.orderId}, '
                                              f'timestamp: {self.timestamp}'
                                              f'status: {self.order_status}')
        return response

    async def create_sell_order(self, price=None) -> list:
        price = self.price_now if price is None else price
        price = math.floor(price * 10 ** self.price_unit) / 10 ** self.price_unit
        sell_coin_number = math.floor(
            self.wallet_free_commodity * 10 ** self.commodity_coin_unit) / 10 ** self.commodity_coin_unit
        response = self._exchange.create_order(
            f'{self._symbol}', 'limit', 'sell', sell_coin_number, price)
        print(f"sell response: {response}")
        self.timestamp = response['timestamp']
        self.order_status = response['status']
        print('creat sell order successful  ', f'order id: {self.orderId},'
                                               f' timestamp: {self.timestamp}'
                                               f'status : {self.order_status}')
        return response

    async def cancelOrder(self):
        response = self._exchange.cancel_order(self.orderId, self._symbol)
        self.timestamp = response['timestamp']
        self.order_status = response['status']
        print('had cancel order successful  ', f'order id: {self.orderId},'
                                               f' timestamp: {self.timestamp}'
                                               f'status : {self.order_status}')
        return response

    @retry(stop_max_attempt_number=5)
    def auto_rich_model(self, transaction_model=False):
        try:

            buy_point = 0
            sell_point = 0
            # highest_point = 0.02
            # lowest_point = 0.005
            translate_times = 0
            reference_point = 0

            having_order = False
            # least_effective_change_percent = 0.001
            # reference_change_p0_p1 = 0

            satisfy_buy_percent = 0.005
            satisfy_sell_percent = 0.0035
            deduction_charge = 0.999

            loop = asyncio.get_event_loop()

            price_0 = loop.create_task(self.GetTickerPrice())
            loop.run_until_complete(price_0)
            wallet_query = loop.create_task(self.fetch_balance())
            loop.run_until_complete(wallet_query)
            time.sleep(60)
            price_1 = loop.create_task(self.GetTickerPrice())
            loop.run_until_complete(price_1)

            price_0 = price_0.result()
            price_1 = price_1.result()
            reference_point = price_0 if price_0 > price_1 else price_1
            time.sleep(60)

            start_principal = self.wallet_free_principal
            start_commodity = self.wallet_free_commodity

            start_point = start_commodity * self.price_now + start_principal

            while True:

                price_query = loop.create_task(self.GetTickerPrice())
                loop.run_until_complete(price_query)

                # self.price_now = price_query.result()
                # reference_change_p0_p1 = abs((price_1 - price_0) / price_1)

                if not having_order and self.wallet_free_principal > 10:

                    # 买入条件
                    if price_1 < self.price_now and reference_point / self.price_now - 1 > satisfy_buy_percent:
                        buy_point = reference_point = self.price_now
                        loop.run_until_complete(loop.create_task(self.create_buy_order()))
                        loop.run_until_complete(loop.create_task(self.fetch_balance()))
                        print(f"buy point: {buy_point} ")
                        having_order = True
                    # 参考点选取
                    elif price_0 < price_1:
                        reference_point = price_1

                # 卖出条件
                if having_order:
                    loop.run_until_complete(loop.create_task(self.fetch_balance()))

                    def sell_it():
                        nonlocal sell_point, reference_point
                        sell_point = reference_point = buy_point * (1 + satisfy_sell_percent)
                        loop.run_until_complete(loop.create_task(self.create_sell_order(sell_point)))
                        loop.run_until_complete(loop.create_task(self.fetch_balance()))
                        nonlocal translate_times
                        translate_times += 1
                        print("translate times: ", translate_times)
                        print(f"buy point {buy_point}, sell point {sell_point}, benefit : {sell_point / buy_point - 1}")

                    if self.wallet_free_commodity * self.price_now > 10:
                        sell_it()
                    if self.wallet_free_principal > 10:
                        having_order = False

                    # # 一般条件
                    # if self.price_now / buy_point - 1 > satisfy_sell_percent \
                    #         and (price_1 - self.price_now) / self.price_now > least_effective_change_percent:
                    #     sell_it()
                    # # 止盈
                    # elif self.price_now / buy_point - 1 > highest_point:
                    #     sell_it()
                price_0, price_1 = price_1, self.price_now
                time.sleep(60)

            print(str(price_query.result()))
            print(wallet_query.result())
            print(self._symbol,
                  self.commodity_coin_name,
                  self.principal_coin_name,

                  self.timestamp,

                  self.wallet_free_principal,
                  self.wallet_free_commodity,

                  self.price_now,
                  self.buy_point,
                  self.sell_point,
                  self.reference_point,
                  self.reduce_point,
                  self.increase_point,
                  self.orderId)

        except Exception:
            raise Exception


test_t = TransactionCurrency('BNB/BUSD')
test_t.auto_rich_model()
