import numpy as np
from matplotlib import pyplot as plt

from log_read import *

bid_list = np.zeros((10000), dtype=float)
ask_list = np.zeros((10000), dtype=float)
list1 = find_keyword('bid', '../logs/522doge_log.txt')

print(list1)
y_axis = []
x_axis = []
index = 0
for i, num in enumerate(list1):
    if i % 6 == 0:
        bid_list[index] = num
        x_axis.append(index)
        y_axis.append(num)
        index += 1
    #     print(y_axis)
    # if i>20:
    #     break
    # print(i,bid_list[index])

plt.plot(x_axis, y_axis)
plt.show()

buy_point = []
sell_point = 0.0
flag = 0
reference_point = bid_list[0]
alpha = 0.0022
beta = 0.001
gamma = -0.0025
i = 1

coin_number = 0.0
money = 5000.0
start = money

miss_opportunity = 0
count = 0
print(index)

while i < index:
    if bid_list[i - 1] < bid_list[i]:
        reference_point = bid_list[i]
    if (bid_list[i] - reference_point) / reference_point < gamma and money > 100.0:  # buy
        buy_point.append(bid_list[i])
        coin_number = money * (1 - beta) / bid_list[i]
        money = 0.0
        count += 1
        reference_point = bid_list[i]
        print("buy it, price is: ", bid_list[i])
    if len(buy_point) > 0:  # sell
        if (bid_list[i] - buy_point[-1]) / bid_list[i] > alpha:
            transfer_coin_money = buy_point.pop()
            money = coin_number * (1 - beta) * bid_list[i]
            coin_number = 0.0
            gamma -= 0.001
            reference_point = bid_list[i]
            print("serial: ", i, "money: ", money, "coin: ", coin_number, "sell price: ", bid_list[i], "buy price: ",
                  transfer_coin_money, "percent: ")
            print("sell it, price is: ", bid_list[i], "percent is: ",
                  (bid_list[i] - transfer_coin_money) / transfer_coin_money)

        # print('miss the opportunity')
        miss_opportunity += 1
    i += 1

print("\n")
print(bid_list[-1])
print("money: ", money, "coin: ", coin_number,
      "\ntotal price: ", money + coin_number * bid_list[index - 1]
      , "\ntotal percent: ", (money - start) / start,
      "\ntransaction times:", count, "miss opportunity times: ", miss_opportunity)
