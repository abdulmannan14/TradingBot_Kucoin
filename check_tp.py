import time
import requests
import hashlib
import hmac


# MEXC API Endpoints and Auth
API_KEY = 'mx0vglWlMkPhfE38aZ'
API_SECRET = '4d99e24697e14a0e94ff23e9588b6dd4'

# BASE_URL = 'https://api.mexc.com'  # Spot trading URL (for spot trading API)
BASE_URL = 'https://contract.mexc.com'  # Futures trading URL (for futures trading API)


def check_tp(pair, order_id, tp_price):
    """Check if the take profit price is hit for the given order."""
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
        response = requests.get(endpoint, params=params, headers=headers)
        data = response.json()

        if data['status'] == 'FILLED':  # Check if the order is completely filled
            print(f"Order {order_id} take profit reached at {tp_price}")
            return True

        # Check if current price has hit TP (optional for manual TP checks)
        current_price = get_current_price(pair)
        if (data['side'] == 'BUY' and current_price >= tp_price) or (
                data['side'] == 'SELL' and current_price <= tp_price):
            print(f"Take profit reached for order {order_id} at {tp_price}")
            return True

        return False

    except Exception as e:
        print(f"Error checking take profit: {e}")
        return False

