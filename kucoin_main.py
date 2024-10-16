import time
from get_current_price_new import get_current_price
from place_limit_order_new import place_limit_order
from check_tp_new import check_tp
from cancel_order_new import cancel_order


# Main Trading Bot Logic
def trade_bot(pair, A_percent, B_percent, countdown, amount):
    """Main trading bot logic with hedging enabled."""
    while True:
        # Get the current market price P
        current_price = get_current_price(pair)
        if not current_price:
            print("Error fetching current price, skipping iteration...")
            continue

        # Calculate entry prices using A%
        long_entry_price = current_price * (1 - A_percent / 100)
        short_entry_price = current_price * (1 + A_percent / 100)

        # Round prices to 0.1 decimal places
        long_entry_price = round(long_entry_price, 1)
        short_entry_price = round(short_entry_price, 1)

        print(f"Long Entry Price: {long_entry_price}, Short Entry Price: {short_entry_price}")

        # Calculate take-profit prices using B%
        long_tp_price = current_price * (1 + B_percent / 100)
        short_tp_price = current_price * (1 - B_percent / 100)

        # Round prices to 0.1 decimal places
        long_tp_price = round(long_tp_price, 1)
        short_tp_price = round(short_tp_price, 1)

        print(f"Take Profit Long Entry Price: {long_tp_price}, Take Profit Short Entry Price: {short_tp_price}")

        # Place long and short orders (hedging enabled)
        long_order = place_limit_order(pair, 'buy', long_entry_price, amount)
        short_order = place_limit_order(pair, 'sell', short_entry_price, amount)

        if not long_order or not short_order:
            print("Error placing orders, retrying...")
            continue

        start_time = time.time()

        # Monitor the orders
        while True:
            # Check if TP for the long order is reached
            if check_tp(long_order['orderId'], long_tp_price, pair):
                cancel_order(short_order['orderId'])
                print("Long TP hit, closing short order.")
                break

            # Check if TP for the short order is reached
            if check_tp(short_order['orderId'], short_tp_price, pair):
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


# Example usage:
pair = "XBTUSDM"  # KuCoin BTC perpetual futures
A_percent = 1  # +/-1% around market price for entry
B_percent = 2  # +/-2% around market price for take profit
countdown = 300  # 5 minutes countdown
amount = 50  # Amount to trade
current_price = get_current_price(pair)
if current_price:
    trade_bot(pair, A_percent, B_percent, countdown, amount)
else:
    print("Error fetching current price, exiting...")
