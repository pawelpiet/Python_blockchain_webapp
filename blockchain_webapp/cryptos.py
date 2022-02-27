import apikey
import requests

def giveCryptos():
    headers = {
    'X-CMC_PRO_API_KEY' : apikey.key,
    'Accepts': 'application/json'
    }

    coins_url ='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'


    data = {
    'start' : '1',
    'limit': '20',
    'convert': 'USD'
    }

    json = requests.get(coins_url,params=data,headers=headers).json()

    ourCoins = json['data']
    
    for coin in ourCoins:
        print(coin['symbol'], coin['quote']['USD']['price'])
        return coin['symbol'], coin['quote']['USD']['price']
