import time
import hmac
import hashlib
import base64
import requests
import json
from config import API_KEY, API_SECRET, API_PASSPHRASE, BASE_URL

encoded_passphrase = base64.b64encode(
    hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())


# Function to create signature
def create_signature(secret, str_to_sign):
    return base64.b64encode(
        hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest()
    ).decode()


# Get current timestamp in milliseconds
def get_timestamp():
    return str(int(time.time() * 1000))


# Function to place a limit order
def place_limit_order(symbol, side, price, quantity):
    # API endpoint to place an order
    endpoint = '/api/v1/orders'

    # Prepare the request body (order data)
    order_data = {
        "clientOid": str(int(time.time() * 1000)),  # Unique client order ID (use timestamp for simplicity)
        "side": side,  # "buy" or "sell"
        "symbol": symbol,  # Trading pair, e.g., "XBTUSDM"
        "type": "limit",  # Limit order
        "price": price,  # The price you want to place the limit order at
        "size": quantity,  # Quantity of the order
        "leverage": 20,  # Example leverage, you can change it
        "marginMode": "ISOLATED",  # Margin mode can be "ISOLATED" or "CROSS"
        "timeInForce": "GTC"  # Good 'Til Canceled (you can use other values like IOC, FOK)
    }

    # Prepare the signature
    timestamp = get_timestamp()
    str_to_sign = timestamp + 'POST' + endpoint + json.dumps(order_data)
    signature = create_signature(API_SECRET, str_to_sign)

    # Headers with API credentials and signature
    headers = {
        'KC-API-KEY': API_KEY,
        'KC-API-SIGN': signature,
        'KC-API-TIMESTAMP': timestamp,
        'KC-API-PASSPHRASE': encoded_passphrase,
        'KC-API-KEY-VERSION': '2',
        'Content-Type': 'application/json'
    }

    # Make the API request
    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=order_data)
    data = response.json()

    if data['code'] == '200000':
        return response.json()
    else:
        print(data)
        return None
