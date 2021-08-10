import types


class Strategy:
    def __init__(self, order=None, sell=None):
        self.name = 'Strategy Example 0'
        if order is not None:
            self.order = types.MethodType(order, self)
        if sell is not None:
            self.sell = types.MethodType(sell, self)

    def order(self):
        is_order = False
        return is_order

    def sell(self):
        is_sell = False
        return is_sell


def order_strategy():
    operation = True
    a = 1
    b = 2
    if a == b:
        return operation
    else:
        return not operation


def sell_strategy():
    operation = True
    a = 1
    b = 2
    if a == b:
        return operation
    else:
        return not operation


strategy1 = Strategy(order=order_strategy(), sell=sell_strategy())
