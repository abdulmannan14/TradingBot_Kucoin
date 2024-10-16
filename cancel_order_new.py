import time
import requests
import hashlib
import hmac
import base64
from config import API_KEY, API_SECRET, API_PASSPHRASE, BASE_URL


def create_kucoin_futures_signature(api_secret, api_passphrase, method, endpoint, params, timestamp):
    """Create the signature for KuCoin Futures API."""
    str_to_sign = f"{timestamp}{method}{endpoint}{params}"
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest()).decode()
    return signature


def cancel_order(pair, order_id):
    """Cancel an existing order using the KuCoin Futures API."""
    endpoint = f"/api/v1/orders/{order_id}"
    url = f"{BASE_URL}{endpoint}"

    # KuCoin Futures requires the request method (DELETE in this case) and a timestamp
    method = "DELETE"
    timestamp = str(int(time.time() * 1000))

    # Parameters for the request (none for DELETE method)
    params = f"?symbol={pair}&timestamp={timestamp}"

    # Generate the signature
    signature = create_kucoin_futures_signature(API_SECRET, API_PASSPHRASE, method, endpoint, '', timestamp)

    # Headers for the request
    headers = {
        'KC-API-KEY': API_KEY,
        'KC-API-SIGN': signature,
        'KC-API-TIMESTAMP': timestamp,
        'KC-API-PASSPHRASE': API_PASSPHRASE,
        'KC-API-KEY-VERSION': '2',  # Key version for KuCoin Futures
        'Content-Type': 'application/json'
    }

    try:
        response = requests.delete(url + params, headers=headers)
        data = response.json()

        if 'data' in data and data['data'] is not None:
            print(f"Order {order_id} canceled successfully")
            return data['data']
        else:
            print(f"Error canceling order: {data}")
            return None

    except Exception as e:
        print(f"Error canceling order: {e}")
        return None
