import time
import requests
import hashlib
import hmac


def get_current_price(pair, BASE_URL='https://api-futures.kucoin.com'):
    """Get the current price for the trading pair from the KuCoin Futures API."""
    endpoint = f"{BASE_URL}/api/v1/ticker"
    params = {'symbol': pair}

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        return float(data['data']['price'])  # Return current price as a float
    except Exception as e:
        print(f"Error getting current price: {e}")
        return None
