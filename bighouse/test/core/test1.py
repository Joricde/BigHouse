import numpy as np
import json
import matplotlib.pyplot as plt
from operation.log_read import *

bid_list = np.zeros((10000), dtype=float)
ask_list = np.zeros((10000), dtype=float)
list1 = find_keyword('bid', '../logs/522btc_log.txt')
y_axis = []
x_axis = []
index = 0
for i, num in enumerate(list1):
    if i % 6 == 0:
        bid_list[index] = num
        x_axis.append(index)
        y_axis.append(num)
        index += 1
        # print(i,bid_list[index])

plt.plot(x_axis, y_axis)
plt.show()

buy_point = 0.0
flag = 0
temp_point = bid_list[0]
highest_point = 0.0
count = 0

alpha = 0.004
beta = 0.003
lam = 0.999
i = 2
buy_time = 0
sell_time = 0

money = 5000
start = money

print(index)

while i < index:

    if flag == 0:
        if bid_list[i - 1] < bid_list[i - 2]:

            if 1 - bid_list[i - 1] / temp_point > 0.002599 and bid_list[i] / bid_list[i - 1] - 1 > alpha:
                flag = 1
                buy_point = bid_list[i]
                buy_time = i
                highest_point = bid_list[i]
                money = lam * money
        else:
            temp_point = bid_list[i - 1]
            print(temp_point)

    else:
        if (bid_list[i] < bid_list[i - 1] and (
                highest_point != buy_point and (
                highest_point - bid_list[i] > 0.2599 * (highest_point - buy_point) or
                1 - bid_list[i] / bid_list[i - 1] > beta))) \
                or (bid_list[i] > bid_list[i - 1] and bid_list[i] / buy_point - 1 > 0.02):
            flag = 0
            count += 1
            money = money * (bid_list[i] / buy_point)
            temp_point = bid_list[i]
            money = lam * money
            print(buy_time, i, money, buy_point, bid_list[i], bid_list[i] / buy_point - 1)
        if bid_list[i] > highest_point:
            highest_point = bid_list[i]
    i += 1

print(money, money / start - 1, count)
