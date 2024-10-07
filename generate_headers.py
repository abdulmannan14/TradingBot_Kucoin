import time
import requests
import hmac
import hashlib
import base64
import json

API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
API_PASSPHRASE = 'your_api_passphrase'
BASE_URL = 'https://api-futures.kucoin.com'

# Generate headers for API authentication
def generate_headers():
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/status'
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())

    headers = {
        "KC-API-KEY": API_KEY,
        "KC-API-SIGN": signature.decode(),
        "KC-API-TIMESTAMP": str(now),
        "KC-API-PASSPHRASE": passphrase.decode(),
        "KC-API-KEY-VERSION": "2"
    }
    return headers
