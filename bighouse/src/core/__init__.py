import abc


class Model(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def order(self):
        """
        implement order method
        """
        pass

    @abc.abstractmethod
    def sell(self):
        """
        implement sell method
        """

        pass


class DataSet(object):
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
