# from pandas.io.json import json_normalize
from crypto_tools import request, API_URL


def printassets(assets):
    """ Prints available assets - accepts asset json object """
    for ass in assets:
        print(f'{ass.name: <{25}} {ass.symbol: <7} {ass.route}')


def listassets():
    """returns a json object with all available assets """
    assets = request(API_URL + "assets")
    return assets


def printasset(asset):
    """prints asset details - accepts assset list"""
    for mar in asset.markets.base:
        print(f'{mar.exchange: <10} {mar.pair: <20} {mar.active} {mar.route}')


def getasset(asset):
    """returns details about asset"""
    asset = request(API_URL + "assets/" + asset)
    return asset


def printpairs(pairs):
    """prints pairs"""
    for pair in pairs:
        print(f'{pair.base.name:20} {pair.symbol: <30} {pair.route}')


def listpairs():
    """returns index of available pairs"""
    pairs = request(API_URL + "pairs")
    return pairs


def printpair(pair):
    """prints pair detail view"""
    print(f'{pair.symbol} {pair.base.name} {pair.quote.name}')
    print("Markets:")
    for market in pair.markets:
        print(f'{market.exchange: <10} {market.active: <5}')


def getpair(pair):
    """Returns pair details - json object"""
    pair = request(API_URL + "pairs/" + pair)
    return pair


def printexchanges(exchanges):
    """ Prints available exchanges - accepts exchange json object """
    # df = json_normalize(exchanges)
    # print(df.loc[df.active == 1])
    maxl = 20
    for ex in exchanges:
        print(f'{ex.name: <{maxl}} {ex.symbol: <{maxl}}'
              f' {ex.route: <{maxl}}')


def listexchanges():
    """returns a json object with all available exchanges """
    exchanges = request(API_URL + "exchanges")
    return exchanges


def printmarkets(markets):
    """Print markets sorted by exchange"""
    for mar in sorted(markets, key=lambda m: (m.exchange, m.pair)):
        print(f'{mar.exchange: <15} {mar.pair: <25} {mar.route}')
    print("Total:", len(markets))


def listmarkets(exchange=None):
    """returns a namedtuple with all available markets"""
    if exchange:
        markets = request(API_URL + "markets/" + exchange)
    else:
        markets = request(API_URL + "markets")
    return markets


def printprices(prices):
    """prints all prices"""
    for key, value in sorted(prices.items()):
        print(f'{key: <40} {value}')


def getallprices():
    """ get all prices in a namedtupel object"""
    prices = request(API_URL + "markets/prices", False)
    return prices
