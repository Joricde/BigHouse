import asyncio
import time
import logging

import numpy as np
from matplotlib import pyplot as plt

from operation.log_read import find_keyword

list_price = find_keyword('bid', '../logs/2021-05-29BTCBUSD_price_data.log')
bid_list = np.zeros(1000000, dtype=float)
ask_list = np.zeros(1000000, dtype=float)
print(list_price)

y_axis = []
x_axis = []
index = 0
for i, num in enumerate(list_price):
    if i % 6 == 0:
        bid_list[index] = num
        x_axis.append(index)
        y_axis.append(num)
        index += 1
    #     print(y_axis)
    # if i>20:
    #     break
    # print(i,bid_list[index])


# plt.plot(x_axis, y_axis)
# plt.show()


def auto_rich_test(transaction_model=False):
    global index

    buy_point = 0
    sell_point = 0
    stop_profit = 0.02
    stop_loss = -0.01
    translate_times = 0

    locked_times = 0
    having_order = False
    least_effective_change_percent = 0.0003

    distance_reference_point = 0.003
    satisfy_buy_percent = 0.003
    satisfy_sell_percent = 0.003
    deduction_charge = 0.999

    price_0 = list_price[0]
    price_1 = list_price[1]
    price_now = list_price[2]
    highest_point_buying = 0.0
    fetch_price_times = 2
    # print(price_0, price_1, price_now)
    reference_point = price_1 if price_0 < price_1 else price_0
    # print(reference_point)

    test_wallet_free_principal = 200
    test_wallet_free_commodity = 0
    start_principal = 200
    start_commodity = 0
    start_point_value = start_commodity * price_now + start_principal

    while fetch_price_times < index:
        if not having_order:

            if price_0 > price_1:

                if 1 - price_1 / reference_point > distance_reference_point and \
                        price_now / price_1 - 1 > satisfy_buy_percent:
                    buy_point = price_now
                    # loop.run_until_complete(loop.create_task(self.create_buy_order()))
                    # loop.run_until_complete(loop.create_task(self.fetch_balance()))
                    test_wallet_free_commodity += test_wallet_free_principal / price_now * deduction_charge
                    test_wallet_free_principal -= test_wallet_free_principal

                    # print(f"buy_point: {buy_point}")
                    having_order = True

            else:
                # elif reference_change_p0_p1 > least_effective_change_percent \
                # and price_1 > price_now and price_1 > price_0:
                reference_point = price_1
                print("reference point: ", reference_point)

        # 卖出条件
        elif having_order:

            if (price_now < price_1 and (highest_point_buying != buy_point and (
                    highest_point_buying - price_now > distance_reference_point * 100 * (
                    highest_point_buying - buy_point) or
                    1 - price_now / price_1 > satisfy_sell_percent))) or \
                    (price_now > price_now and price_now / buy_point > highest_point_buying - 1 > stop_profit):
                having_order = False
                translate_times += 1
                test_wallet_free_principal += test_wallet_free_commodity * price_now * deduction_charge
                test_wallet_free_commodity -= test_wallet_free_commodity
                reference_point = price_now

            else:
                locked_times += 1

            if price_now > highest_point_buying:
                highest_point_buying = price_now

        fetch_price_times += 1
        price_0, price_1, price_now = price_1, price_now, list_price[fetch_price_times]
        start_point_value = start_commodity * price_now + start_principal

    print(f"start: {start_point_value}, now: {test_wallet_free_principal + test_wallet_free_commodity * price_now}")


auto_rich_test()
