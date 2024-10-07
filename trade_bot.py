import time
import requests
import hashlib
import hmac
from get_current_price import get_current_price
from place_limit_order import place_limit_order
from cancel_order import cancel_order
from check_tp import check_tp


def trade_bot(pair, A_percent, B_percent, countdown, amount):
    """Main trading bot logic with hedging enabled."""

    while True:
        # Get the current market price P
        current_price = get_current_price(pair)

        if current_price is None:
            print(f"Error fetching the price for {pair}. Retrying...")
            time.sleep(5)
            continue

        # Calculate entry prices using A%
        long_entry_price = current_price * (1 - A_percent / 100)
        short_entry_price = current_price * (1 + A_percent / 100)

        # Calculate take profit prices using B%
        long_tp_price = current_price * (1 + B_percent / 100)
        short_tp_price = current_price * (1 - B_percent / 100)

        # Place long and short orders (hedging enabled)
        long_order = place_limit_order(pair, 'BUY', long_entry_price, amount)
        short_order = place_limit_order(pair, 'SELL', short_entry_price, amount)

        # Check if the order placement succeeded
        if long_order is None or short_order is None:
            print("Order placement failed, retrying...")
            time.sleep(5)
            continue

        start_time = time.time()

        # Monitor the orders
        while True:
            # Check if TP for the long order is reached
            if check_tp(pair, long_order['orderId'], long_tp_price, 'BUY'):
                cancel_order(short_order['orderId'])
                print("Long TP hit, closing short order.")
                break

            # Check if TP for the short order is reached
            if check_tp(pair, short_order['orderId'], short_tp_price, 'SELL'):
                cancel_order(long_order['orderId'])
                print("Short TP hit, closing long order.")
                break

            # Check if countdown has expired
            if time.time() - start_time > countdown:
                cancel_order(long_order['orderId'])
                cancel_order(short_order['orderId'])
                print("Countdown expired, restarting orders.")
                break

        # Sleep a bit before restarting (optional)
        time.sleep(5)


pair = "BTCUSDT"
A_percent = 1.0  # +/-1% around market price for entry
B_percent = 2.0  # +/-2% around market price for take profit
countdown = 300  # 5 minutes countdown
amount = 0.001  # Amount to trade

trade_bot(pair, A_percent, B_percent, countdown, amount)
