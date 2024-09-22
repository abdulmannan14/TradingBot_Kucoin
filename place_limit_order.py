import time
import requests
import hashlib
import hmac

# MEXC API Endpoints and Auth
API_KEY = 'mx0vglWlMkPhfE38aZ'
API_SECRET = '4d99e24697e14a0e94ff23e9588b6dd4'

# BASE_URL = 'https://api.mexc.com'  # Spot trading URL (for spot trading API)
#
#
BASE_URL = 'https://contract.mexc.com'  # Futures trading URL (for futures trading API)


def place_limit_order(pair, side, price, amount):
    """Place a limit order (either 'BUY' or 'SELL') at the specified price."""
    endpoint = f"{BASE_URL}/api/v3/order"

    # Generate the payload for the request
    params = {
        'symbol': pair,
        'side': side,  # 'BUY' or 'SELL'
        'type': 'LIMIT',
        'timeInForce': 'GTC',  # Good till canceled
        'quantity': amount,
        'price': price,
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
        print("THUIS IS ENDPOINT++++++", endpoint)
        print("THUIS IS Params++++++", params)
        print("THUIS IS Header++++++", headers)
        response = requests.post(endpoint, params=params, headers=headers)
        data = response.json()
        print("this is data======1", data)

        if 'orderId' in data:
            print(f"Order placed successfully: {data['orderId']}")
            return data  # Return the order data including orderId
        else:
            print(f"Error placing order: {data}")
            return None

    except Exception as e:
        print(f"Error placing limit order: {e}")
        return None
