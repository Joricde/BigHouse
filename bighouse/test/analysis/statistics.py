import numpy as np
import json
import matplotlib.pyplot as plt
from operation.log_read import *


class data:
    def __init__(self, start_index, end_index, start_price, end_price, percentage):
        self.start_index = start_index
        self.end_index = end_index
        self.start_price = start_price
        self.end_price = end_price
        self.percentage = percentage


rising_list = [list() for i in range(11)]
profit_list = [list() for i in range(11)]
deficit_list = [list() for i in range(11)]
profit_bp_list = [list() for i in range(11)]
profit_sp_list = [list() for i in range(11)]
deficit_bp_list = [list() for i in range(11)]
deficit_sp_list = [list() for i in range(11)]

y_axis = []
x_axis = []

bid_list = []
data_list = []

list1 = find_keyword('bid', '\\\\OpenWrt\\share\\logs\\2021-05-25BTCBUSD_price_data.log')

index = 0

for i, num in enumerate(list1):
    if i % 6 == 0:
        # print(index, num)
        bid_list.append(num)
        x_axis.append(index)
        y_axis.append(num)
        index += 1

price_0 = bid_list[0]
price_1 = bid_list[1]
price_now = 0

rising = 0
descending = 0
high_point = 0
low_point = 0

if price_0 > price_1:
    high_point = 0
    low_point = 1
    descending = 1

else:
    high_point = low_point = 0
    descending = 0

i = 2

path = 0

while i < index:
    price_now = bid_list[i]

    if descending:
        if price_now < price_1:
            low_point = i
        else:
            descending = 0

    if price_1 > price_0 and price_1 > price_now:
        d = data(low_point, i - 1, bid_list[low_point], price_1, price_1 / bid_list[low_point] - 1)
        data_list.append(d)

        p = (price_1 / bid_list[low_point] - 1) * 1000

        if 0 <= p < 1:
            rising_list[0].append(d)
        elif 1 <= p < 2:
            rising_list[1].append(d)
        elif 2 <= p < 3:
            rising_list[2].append(d)
        elif 3 <= p < 4:
            rising_list[3].append(d)
        elif 4 <= p < 5:
            rising_list[4].append(d)
        elif 5 <= p < 6:
            rising_list[5].append(d)
        elif 6 <= p < 7:
            rising_list[6].append(d)
        elif 7 <= p < 8:
            rising_list[7].append(d)
        elif 8 <= p < 9:
            rising_list[8].append(d)
        elif 9 <= p < 10:
            rising_list[9].append(d)
        else:
            rising_list[10].append(d)

        print(low_point, i - 1, price_1 / bid_list[low_point] - 1)

        p = (bid_list[d.end_index + 1] / bid_list[d.start_index + 1] - 1) * 1000

        pos = 0

        if p >= 0 and p < 1:
            pos = 0
        elif p >= 1 and p < 2:
            pos = 1
        elif p >= 2 and p < 3:
            pos = 2
        elif p >= 3 and p < 4:
            pos = 3
        elif p >= 4 and p < 5:
            pos = 4
        elif p >= 5 and p < 6:
            pos = 5
        elif p >= 6 and p < 7:
            pos = 6
        elif p >= 7 and p < 8:
            pos = 7
        elif p >= 8 and p < 9:
            pos = 8
        elif p >= 9 and p < 10:
            pos = 9
        elif p >= 10:
            pos = 10
        else:
            pos = -1

        if pos != -1:
            profit_list[pos].append(d)
            profit_bp_list[pos].append(1 - (bid_list[d.start_index] / bid_list[d.start_index - 1]))
            profit_sp_list[pos].append(1 - (bid_list[d.end_index + 1] / bid_list[d.end_index]))

        p = (1 - bid_list[d.end_index + 1] / bid_list[d.start_index + 1]) * 1000

        if p >= 0 and p < 1:
            pos = 0
        elif p >= 1 and p < 2:
            pos = 1
        elif p >= 2 and p < 3:
            pos = 2
        elif p >= 3 and p < 4:
            pos = 3
        elif p >= 4 and p < 5:
            pos = 4
        elif p >= 5 and p < 6:
            pos = 5
        elif p >= 6 and p < 7:
            pos = 6
        elif p >= 7 and p < 8:
            pos = 7
        elif p >= 8 and p < 9:
            pos = 8
        elif p >= 9 and p < 10:
            pos = 9
        elif p >= 10:
            pos = 10
        else:
            pos = -1

        if pos != -1:
            deficit_list[pos].append(d)
            deficit_bp_list[pos].append(1 - (bid_list[d.start_index] / bid_list[d.start_index - 1]))
            deficit_sp_list[pos].append(1 - (bid_list[d.end_index + 1] / bid_list[d.end_index]))

        descending = 1
        low_point = i

    price_0, price_1 = price_1, bid_list[i]

    i += 1

print(len(data_list))
print("\n")

i = 0
while i < 11:
    print((str)(i / 1000))
    print(len(rising_list[i]))

    print("profit:", len(profit_list[i]))

    t1 = np.array(profit_bp_list[i])
    t2 = np.array(profit_sp_list[i])

    print("buy_percent")
    print("avg: ", np.mean(t1), "std: ", np.std(t1))
    print("sell_percent")
    print("avg: ", np.mean(t2), "std: ", np.std(t2), "\n")

    print("deficit:", len(deficit_list[i]))

    t1 = np.array(deficit_bp_list[i])
    t2 = np.array(deficit_sp_list[i])

    print("buy_percent")
    print("avg: ", np.mean(t1), "std: ", np.std(t1))
    print("sell_percent")
    print("avg: ", np.mean(t2), "std: ", np.std(t2), "\n")

    i += 1
