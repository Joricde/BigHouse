import types
from bighouse import logger
from bighouse.src.core import Model


class ModelImpl(Model):
    def __init__(self, order=None, sell=None):
        self.name = 'Model'
        if order is not None:
            self.order = types.MethodType(order, self)
        if sell is not None:
            self.sell = types.MethodType(sell, self)

    def order(self):
        execute = False
        logger.info("")
        return execute

    def sell(self):
        execute = False
        logger.info("")
        return execute
