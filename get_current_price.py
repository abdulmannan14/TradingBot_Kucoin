import time
import requests
import hashlib
import hmac

# MEXC API Endpoints and Auth
API_KEY = 'mx0vglWlMkPhfE38aZ'
API_SECRET = '4d99e24697e14a0e94ff23e9588b6dd4'

# BASE_URL = 'https://api.mexc.com'  # Spot trading URL (for spot trading API)
BASE_URL = 'https://contract.mexc.com'  # Futures trading URL (for futures trading API)


def get_current_price(pair):
    """Get the current price for the trading pair from the MEXC API."""
    import requests
    url = f"https://contract.mexc.com/api/v1/contract/index_price/{pair}"
    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        return (data['data']['indexPrice'])  # Returning the current price as a float
    except Exception as e:
        print(f"Error getting current price: {e}")
        return None
