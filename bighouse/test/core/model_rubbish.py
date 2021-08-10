from retrying import retry
import logging
from operation.log_read import find_keyword

logging.basicConfig(level=logging.DEBUG)
list_price = find_keyword('bid', '//OpenWrt/share/logs/2021-05-31BNBBUSD_price_data.log')
list_price_6 = []
for _, sixty_seconds in enumerate(list_price):
    if _ % 6 == 0:
        list_price_6.append(sixty_seconds)

logging.debug(list_price)


@retry(stop_max_attempt_number=5)
def auto_rich_test(transaction_model=False):
    price_tack = []
    highest_point_buying = 0
    control_tack_size = 60
    fetch_times = control_tack_size

    stop_profit = 0.02
    increase_percent = 0.002
    distance_point = 0.005
    buy_point = 0
    sell_point = 0
    server_charge = 0.999

    buy_time = 0
    sell_time = 0
    sell_out_time = 0
    buying_status = False

    start_money = 5000
    wallet_principal = 1000
    wallet_commodity = 0
    buy_stack = dict()
    sell_stack = dict()

    logging.info(len(list_price_6))

    reference_point = list_price_6[0]
    total = 0
    for num in range(control_tack_size):
        price_tack.append(list_price_6[num])
        total += list_price_6[num]
        if price_tack[len(price_tack) - 2] < list_price_6[num]:
            reference_point = list_price_6[num]
    avg = total / len(price_tack)

    price0, price1, price_now = \
        list_price_6[control_tack_size - 2], list_price_6[control_tack_size - 1], list_price_6[control_tack_size]

    while fetch_times < len(list_price_6)-1:
        if not buying_status:
            # buy it
            if 1 - price_now / avg > distance_point and price_now / price1 - 1 > 0:
                buy_point = price_now
                buy_stack[fetch_times] = buy_point
                wallet_commodity += wallet_principal / price_now * server_charge + wallet_commodity
                wallet_principal -= wallet_principal
                highest_point_buying = price_now
                buy_time += 1
                logging.info(f"  buy it on {fetch_times}, buy it on {price_now}---------")
                buying_status = True
            elif price0 < price1:
                reference_point = price1
        else:
            def sell_it(info='loss'):
                nonlocal buying_status, wallet_principal, wallet_commodity, price_now, sell_time, reference_point
                nonlocal sell_out_time, sell_point
                wallet_principal += wallet_commodity * price_now * server_charge + wallet_principal
                wallet_commodity -= wallet_commodity
                sell_time += 1
                reference_point = price_now
                sell_point = price_now
                sell_stack[fetch_times] = sell_point
                logging.info(f"sell it on {fetch_times}, sell it on {price_now}, info: {info}")
                sell_out_time = 0
                buying_status = False

            # sell it situation

            # stop profit
            if highest_point_buying < price_now:
                highest_point_buying = price_now
            elif price_now / buy_point - 1 > increase_percent and price_now < price1:
                sell_it('profit increase')
            elif price_now / buy_point - 1 > stop_profit:
                sell_it('stop profit')
            # else:
            #     sell_out_time += 1
            #     if sell_out_time > control_tack_size:
            #         if avg < price_now < price1:
            #             sell_it("time out")
        fetch_times += 1

        price0, price1, price_now = price1, price_now, list_price_6[fetch_times]
        avg += price_now / control_tack_size
        avg -= price_tack.pop(0) / control_tack_size
        price_tack.append(price_now)

    logging.info(
        f"start money:{start_money} now principal: {wallet_principal}, commodity:{wallet_commodity}, "
        f"total money: {wallet_principal + wallet_commodity * price_now}, "
        f"translation times: {sell_time}, ")


auto_rich_test()
