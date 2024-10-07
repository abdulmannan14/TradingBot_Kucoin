import time
import requests
import hashlib
import hmac
from generate_headers import generate_headers


def place_limit_order(pair, side, price, amount, BASE_URL='https://api-futures.kucoin.com'):
    """Place a limit order (either 'BUY' or 'SELL') at the specified price."""
    endpoint = f"{BASE_URL}/api/v1/orders"

    # Order details
    order_data = {
        'clientOid': str(int(time.time() * 1000)),  # Unique ID for this order
        'symbol': pair,
        'side': side.lower(),  # 'buy' for long, 'sell' for short
        'type': 'limit',
        'price': price,
        'size': amount,
        'leverage': '10',  # Set your desired leverage
        'timeInForce': 'GTC'  # Good till canceled
    }

    try:
        headers = generate_headers()
        response = requests.post(endpoint, json=order_data, headers=headers)
        data = response.json()

        if 'orderId' in data['data']:
            print(f"Order placed successfully: {data['data']['orderId']}")
            return data['data']
        else:
            print(f"Error placing order: {data}")
            return None

    except Exception as e:
        print(f"Error placing limit order: {e}")
        return None
