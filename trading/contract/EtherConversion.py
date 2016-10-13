# Convert ether to USD for trading
import requests


def convert(balance):
    r = requests.get('https://coinmarketcap-nexuist.rhcloud.com/api/eth')
    c = r.json()
    capital = c.get('price').get('usd')
    return capital
