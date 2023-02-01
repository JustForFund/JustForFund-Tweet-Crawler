import requests
import os

BASE_URL = 'https://justfor.fund/api/v1'
API_KEY = os.environ['JUSTFORFUND_ALGORITHM_API_KEY']
API_SECRET = os.environ['JUSTFORFUND_ALGORITHM_SECRET_KEY']
HEADERS = {'API-KEY': API_KEY, 'API-SECRET': API_SECRET}

def create_trading_signal(algorithm_id, symbol, portfolio_ratio_investment, order_type, side, time_in_force):
    data = {
        "algorithm_id":algorithm_id,
        "ticker_symbol":symbol,
        "order_type": order_type, 
        "portfolio_ratio_investment": portfolio_ratio_investment, 
        "side":side, 
        "time_in_force":time_in_force
    }
    print(data)
    url = "{}/create_trading_signal".format(BASE_URL)
    print(url)
    print(HEADERS)
    r = requests.post(url, json=data , headers=HEADERS)
    print(r)
    return r
