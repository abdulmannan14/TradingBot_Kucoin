import time
import requests
import hashlib
import hmac



# MEXC API Endpoints and Auth
API_KEY = 'mx0vglWlMkPhfE38aZ'
API_SECRET = '4d99e24697e14a0e94ff23e9588b6dd4'

# BASE_URL = 'https://api.mexc.com'  # Spot trading URL (for spot trading API)
BASE_URL = 'https://contract.mexc.com'  # Futures trading URL (for futures trading API)


def cancel_order(pair, order_id):
    """Cancel an existing order using the MEXC API."""
    endpoint = f"{BASE_URL}/api/v3/order"

    # Generate the payload for the request
    params = {
        'symbol': pair,
        'orderId': order_id,
        'timestamp': int(time.time() * 1000)
    }

    # Add the signature
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params['signature'] = signature

    # Headers for the request
    headers = {
        'X-MEXC-APIKEY': API_KEY
    }

    try:
        response = requests.delete(endpoint, params=params, headers=headers)
        data = response.json()

        if 'orderId' in data:
            print(f"Order {order_id} canceled successfully")
            return data
        else:
            print(f"Error canceling order: {data}")
            return None

    except Exception as e:
        print(f"Error canceling order: {e}")
        return None

