import time
import hmac
import hashlib
import base64
import requests
from get_current_price_new import get_current_price
from config import API_KEY, API_SECRET, API_PASSPHRASE, BASE_URL


def create_kucoin_futures_signature(api_secret, api_passphrase, method, endpoint, params, timestamp):
    """Create the signature and passphrase for KuCoin Futures API."""
    str_to_sign = f"{timestamp}{method}{endpoint}{params}"
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest()).decode()
    passphrase = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest()).decode()
    return signature, passphrase


def check_tp(order_id, tp_price, pair):
    """Check if the take profit price is hit for the given futures order on KuCoin."""
    endpoint = f"/api/v1/orders/{order_id}"
    url = f"{BASE_URL}{endpoint}"

    # KuCoin Futures requires the request method (GET in this case) and a timestamp
    method = "GET"
    timestamp = str(int(time.time() * 1000))

    # Generate the signature
    params = ""
    signature, passphrase = create_kucoin_futures_signature(API_SECRET, API_PASSPHRASE, method, endpoint, params,
                                                            timestamp)

    # Headers for the request
    headers = {
        'KC-API-KEY': API_KEY,
        'KC-API-SIGN': signature,
        'KC-API-TIMESTAMP': timestamp,
        'KC-API-PASSPHRASE': passphrase,
        'KC-API-KEY-VERSION': '2',  # Key version for KuCoin Futures is also version 2
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if data['data']['status'] == 'done':  # Check if the order is filled or canceled
            print(f"Order {order_id} take profit reached at {tp_price}")
            return True

        # Check if current price has hit TP (optional for manual TP checks)
        current_price = get_current_price(pair)  # Implement this function to get the current price
        if (data['data']['side'] == 'buy' and current_price >= tp_price) or (
                data['data']['side'] == 'sell' and current_price <= tp_price):
            print(f"Take profit reached for order {order_id} at {tp_price}")
            return True

        return False

    except Exception as e:
        print(f"Error checking take profit: {e}")
        return False
