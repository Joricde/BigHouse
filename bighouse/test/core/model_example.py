"""
run it to see the effect
"""

import types

from bighouse import logger


class Strategy:
    is_order = False
    is_sell = False

    def __init__(self, order=None, sell=None):
        self.name = 'Strategy Example'
        if order is not None:
            self.order = types.MethodType(order, self)
        if sell is not None:
            self.sell = types.MethodType(sell, self)

    def order(self):
        logger.debug(self.is_order)
        return self.is_order

    def sell(self):
        logger.debug(self.is_sell)
        return self.is_sell


def order_strategy(self):
    operation = True
    a = 1
    b = 2
    if a == b:
        return operation
    else:
        logger.debug("order_Strategy")
        return not operation


def sell_strategy(self):
    operation = True
    a = 1
    b = 2
    if a == b:
        return operation
    else:
        logger.debug("sell_Strategy")
        return not operation


strategy1 = Strategy(order=order_strategy, sell=sell_strategy)
strategy1.sell()
strategy1.order()
