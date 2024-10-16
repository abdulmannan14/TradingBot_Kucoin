import base64
import time
import requests
import hashlib
import hmac
from config import API_KEY, API_SECRET, API_PASSPHRASE, BASE_URL


# Create signature function
def create_signature(secret, str_to_sign):
    return base64.b64encode(
        hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest()
    ).decode()


# Get current timestamp in milliseconds
def get_timestamp():
    return str(int(time.time() * 1000))


# Get current mark price for XBTUSDM
def get_current_price(symbol):
    timestamp = get_timestamp()
    endpoint = f'/api/v1/mark-price/{symbol}/current'

    str_to_sign = timestamp + 'GET' + endpoint
    signature = create_signature(API_SECRET, str_to_sign)

    headers = {
        'KC-API-KEY': API_KEY,
        'KC-API-SIGN': signature,
        'KC-API-TIMESTAMP': timestamp,
        'KC-API-PASSPHRASE': API_PASSPHRASE,
        'KC-API-KEY-VERSION': '2',
        'Content-Type': 'application/json'
    }

    response = requests.get(BASE_URL + endpoint, headers=headers)
    data = response.json()
    # Check for a successful response and return the mark price as a float
    if data['code'] == '200000':  # Assuming '200000' means success
        return float(data['data']['value'])  # Extract and return the price as float
    else:
        print(f"Error fetching price: {data['msg']}")
        return None  # Return None if there's an error
