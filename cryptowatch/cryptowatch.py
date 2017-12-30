#!/usr/sbin/env python3
import argparse
import json
from collections import namedtuple

import requests
import pandas as pd
#from pandas.io.json import json_normalize
from colorama import Fore


API_URL = "https://api.cryptowat.ch/"

allowance = {}


# source: https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
def _json_object_hook(dat):
    """Json hook to convert json object to named tuple
    DO NOT CALL DIRECTLY"""
    return namedtuple('X', dat.keys())(*dat.values())


def json2obj(data):
    """Convert json object to NamedTuple"""
    return json.loads(data, object_hook=_json_object_hook)


def request(url, convert=True):
    """Requests to api and return python object"""
    # pylint: disable=W0603
    global allowance
    req = requests.get(url)
    if convert:
        res = json2obj(req.text).result
        allowance = res.allowance
    else:
        allowance = json2obj(json.dumps(req.json()["allowance"]))
        res = req.json()["result"]

    printallowance()
    return res


def printallowance():
    """prints remaining allowance"""
    rem = int(allowance.remaining)
    cost = int(allowance.cost)
    avg_rem = rem / cost
    print(Fore.YELLOW + "Allowance:" + Fore.LIGHTWHITE_EX)
    print("Cost:", cost)
    print("Remaining:", rem)
    print("AvgRemReq:", avg_rem)
    print()


def printassets(assets):
    """ Prints available assets - accepts asset json object """
    max = 25
    for ass in assets:
        #print(ass.symbol, ass.name, ass.symbol, ass.route)
        print(
            f'{ass.name: <{max}} {ass.symbol: <7} {ass.route}')


def listassets():
    """returns a json object with all available assets """
    assets = request(API_URL + "assets")
    return assets


def printasset(asset):
    """prints asset details - accepts assset list"""
    for a in asset.markets.base:
        print(f'{a.exchange: <10} {a.pair: <20} {a.active} {a.route}')


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
    max = 20
    for ex in exchanges:
        print(f'{ex.name: <{max}} {ex.symbol: <{max}}'
              f' {ex.route: <{max}}')


def listexchanges():
    """returns a json object with all available exchanges """
    exchanges = request(API_URL + "exchanges")
    return exchanges


def printmarkets(markets):
    """Print markets sorted by exchange"""
    for m in sorted(markets, key=lambda m: (m.exchange, m.pair)):
        print(f'{m.exchange: <15} {m.pair: <25} {m.route}')


def listmarkets(exchange=None):
    """returns a namedtuple with all available markets"""
    if exchange:
        markets = request(API_URL + "markets/" + exchange)
    else:
        markets = request(API_URL + "markets")
    return markets


def getmarketpair(exchange, pair):
    """Get's pairs for the selected exchange / pair combinations"""
    p = request(API_URL + "markets/" + exchange + "/" + pair + "/summary")
    return p


def printprices(prices):
    """prints all prices"""
    for key, value in sorted(prices.items()):
        print(f'{key: <40} {value}')


def getallprices():
    """ get all prices in a namedtupel object"""
    prices = request(API_URL + "markets/prices", False)
    return prices


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--listassets", dest="listassets",
                        action="store_true", required=False,
                        help="Get asset index and exit")
    parser.add_argument("-a", "--asset", dest="asset",
                        required=False,
                        help="Get detail info about Asset")

    parser.add_argument("--listpairs", dest="listpairs",
                        action="store_true", required=False,
                        help="Get pair index and exit")
    parser.add_argument("--getpair", dest="getpair",
                        required=False,
                        help="Get pair details and exit")

    parser.add_argument("--listexchanges", dest="listexchanges",
                        action="store_true", required=False,
                        help="Get exchange index and exit")

    parser.add_argument("--listmarkets", dest="listmarkets",
                        action="store_true", required=False,
                        help="Get markets index and exit")

    parser.add_argument("-m", "--market", dest="market", required=False,
                        help="Get available markets / pairs for this exchange")
    parser.add_argument("-p", "--pairs", dest="pairs", nargs="*",
                        help="Pairs to monitor")
    parser.add_argument("--getallprices", dest="getallprices",
                        action="store_true", required=False,
                        help="Get all prices exit")
    args = parser.parse_args()

    if args.listassets:
        printassets(listassets())
        return

    if args.asset:
        printasset(getasset(args.asset))

    if args.listpairs:
        printpairs(listpairs())

    if args.getpair:
        printpair(getpair(args.getpair))

    if args.listexchanges:
        printexchanges(listexchanges())
        return

    if args.listmarkets:
        printmarkets(listmarkets())

    if args.market and not args.pairs:
        markets = listmarkets(args.market)
        printmarkets(markets)

    if args.market and args.pairs:
        for pair in args.pairs:
            print(getmarketpair(args.market, pair))

    if args.getallprices:
        printprices(getallprices())

if __name__ == "__main__":
    pd.options.display.width = 120
    main()
