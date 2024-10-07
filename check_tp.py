import time
import requests
import hashlib
import hmac
from get_current_price import get_current_price


def check_tp(pair, order_id, tp_price, side):
    """Check if the take profit price is hit for the given order."""
    current_price = get_current_price(pair)

    if current_price is None:
        print("Error fetching current price.")
        return False

    # For a long order (BUY), the current price should be >= tp_price to hit TP
    # For a short order (SELL), the current price should be <= tp_price to hit TP
    if (side == 'BUY' and current_price >= tp_price) or (side == 'SELL' and current_price <= tp_price):
        print(f"Take profit reached for order {order_id}. Current price: {current_price}, TP price: {tp_price}")
        return True

    return False
