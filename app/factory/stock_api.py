import requests

API_KEY = 'br796tfrh5r9l4n3o0a0'


def api_response(symbol):
    url = 'https://finnhub.io/api/v1/quote?symbol={}&token={}'
    response = requests.get(url.format(symbol.upper(), API_KEY)).json()
    return response


def get_price(symbol):
    response = api_response(symbol)
    if len(response) != 0:
        price = response['c']
        return price
    else:
        return False
