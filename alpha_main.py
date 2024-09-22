import time
import requests
import hashlib
import hmac
from get_current_price import get_current_price
from place_limit_order import place_limit_order
from check_tp import check_tp
from cancel_order import cancel_order

# MEXC API Endpoints and Auth
API_KEY = 'mx0vglWlMkPhfE38aZ'
API_SECRET = '4d99e24697e14a0e94ff23e9588b6dd4'

# BASE_URL = 'https://api.mexc.com'  # Spot trading URL (for spot trading API)
#
#
BASE_URL = 'https://contract.mexc.com'  # Futures trading URL (for futures trading API)


def trade_bot(pair, A_percent, B_percent, countdown, amount):
    """Main trading bot logic with hedging enabled."""
    while True:
        print("========================ENTEREDDDDDDDD============================")
        # Get the current market price P
        current_price = get_current_price(pair)
        print("this is current price======", current_price)

        # Calculate entry prices using A%
        long_entry_price = current_price * (1 - A_percent / 100)
        short_entry_price = current_price * (1 + A_percent / 100)

        print("long_entry_price=", long_entry_price, "short_entry_price=", short_entry_price)

        # Calculate take profit prices using B%
        long_tp_price = current_price * (1 + B_percent / 100)
        short_tp_price = current_price * (1 - B_percent / 100)
        print("long_tp_price=", long_tp_price, "short_tp_price=", short_tp_price)
        break
        # Place long and short orders (hedging enabled)
        long_order = place_limit_order(pair, 'BUY', long_entry_price, amount)

        print("====================================================")
        print("====================================================")
        print("====================================================")
        print("====================================================")
        short_order = place_limit_order(pair, 'SELL', short_entry_price, amount)
        print("this is long_order======", long_order)
        print("this is short_order======", short_order)

        start_time = time.time()

        # Monitor the orders
        while True:
            # Check if TP for the long order is reached
            if check_tp(long_order['id'], long_tp_price):
                cancel_order(short_order['id'])
                print("Long TP hit, closing short order.")
                break

            # Check if TP for the short order is reached
            if check_tp(short_order['id'], short_tp_price):
                cancel_order(long_order['id'])
                print("Short TP hit, closing long order.")
                break

            # Check if countdown has expired
            if time.time() - start_time > countdown:
                cancel_order(long_order['id'])
                cancel_order(short_order['id'])
                print("Countdown expired, restarting orders.")
                break

        # Sleep a bit before restarting (optional)
        time.sleep(5)


# Example usage:
pair = "BTC_USDT"
A_percent = 1  # +/-1% around market price for entry
B_percent = 10  # +/-2% around market price for take profit
countdown = 300  # 5 minutes countdown
amount = 50  # Amount to trade

price = get_current_price(pair)
print("this is price======", price)
if price:
    print(f"The pair {pair} is not supported.")
    trade_bot(pair, A_percent, B_percent, countdown, amount)
else:
    print("ELSE-------------------")
    # trade_bot(pair, A_percent, B_percent, countdown, amount)

    # hit this url api/v1/contract/ping
    print(requests.get("https://contract.mexc.com/api/v1/contract/ping"))
