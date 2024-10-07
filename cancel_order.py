import time
import requests
import hashlib
import hmac
from generate_headers import generate_headers


def cancel_order(order_id, BASE_URL='https://api-futures.kucoin.com'):
    """Cancel an existing order on KuCoin Futures."""
    endpoint = f"{BASE_URL}/api/v1/orders/{order_id}"

    try:
        headers = generate_headers()
        response = requests.delete(endpoint, headers=headers)
        data = response.json()

        if 'cancelledOrderId' in data['data']:
            print(f"Order {order_id} canceled successfully")
            return data['data']
        else:
            print(f"Error canceling order: {data}")
            return None

    except Exception as e:
        print(f"Error canceling order: {e}")
        return None
