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


def request(url):
    global allowance
    req = requests.get(url)
    res = req.json()
    x = json.loads(req.text, object_hook=lambda d: namedtuple(
        'X', d.keys())(*d.values()))
    print(dir(x.result))
    allowance = res["allowance"]
    printallowance()
    return res["result"]


def printallowance():
    """prints remaining allowance"""
    rem = int(allowance["remaining"])
    cost = int(allowance["cost"])
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
        #print(ass["symbol"], ass["name"], ass["symbol"], ass["route"])
        print(
            f'{ass["name"]: <{max}} {ass["symbol"]: <7} {ass["route"]}')


def listassets():
    """returns a json object with all available assets """
    assets = request(API_URL + "assets")
    return assets


def printasset(asset):
    """prints asset details - accepts assset list"""
    for a in asset["markets"]["base"]:
        print(f'{a["exchange"]: <10} {a["pair"]: <20} {a["active"]} {a["route"]}')


def getasset(asset):
    """returns details about asset"""
    asset = request(API_URL + "assets/" + asset)
    return asset


def printpairs(pairs):
    """prints pairs"""
    for pair in pairs:
        print(f'{pair["base"]["name"]:20} {pair["symbol"]: <30} {pair["route"]}')


def listpairs():
    """returns index of available pairs"""
    pairs = request(API_URL + "pairs")
    return pairs


def printpair(pair):
    """prints pair detail view"""
    print(f'{pair["symbol"]} {pair["base"]["name"]} {pair["quote"]["name"]}')
    print("Markets:")
    for market in pair["markets"]:
        print(f'{market["exchange"]: <10} {market["active"]: <5}')


def getpair(pair):
    """Returns pair details - json object"""
    pair = request(API_URL + "pairs/" + pair)
    return pair


def printexchanges(exchanges):
    """ Prints available exchanges - accepts exchange json object """
    #df = json_normalize(exchanges)
    #print(df.loc[df.active == 1])
    max = 20
    for ex in exchanges:
        print(f'{ex["name"]: <{max}} {ex["symbol"]: <{max}}'
              f' {ex["route"]: <{max}}')


def listexchanges():
    """returns a json object with all available exchanges """
    exchanges = request(API_URL + "exchanges")
    return exchanges


def printmarkets(markets):
    for m in markets:
        print(m["exchange"], m["pair"],  m["route"])


def getmarkets(exchange):
    """Gets markets for selected exchange"""
    markets = request(API_URL + "markets/" + exchange)
    return markets


def getmarketpair(exchange, pair):
    """Get's pairs for the selected exchange / pair combinations"""
    p = request(API_URL + "markets/" + exchange + "/" + pair + "/summary")
    return p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--listassets", dest="listassets",
                        action="store_true", required=False,
                        help="Get asset index and exit")
    parser.add_argument("-a", "--assets", dest="assets", nargs="*",
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
                        help="Get exchange list and exit")

    parser.add_argument("-m", "--market", dest="market", required=False)
    parser.add_argument("-p", "--pairs", dest="pairs", nargs="*",
                        help="Pairs to monitor")
    args = parser.parse_args()

    if args.listassets:
        printassets(listassets())
        return

    if args.assets:
        for asset in args.assets:
            printasset(getasset(asset))

    if args.listpairs:
        printpairs(listpairs())

    if args.getpair:
        printpair(getpair(args.getpair))

    if args.listexchanges:
        printexchanges(listexchanges())
        return

    if args.market and not args.pairs:
        markets = getmarkets(args.market)
        printmarkets(markets)

    if args.market and args.pairs:
        for pair in args.pairs:
            print(getmarketpair(args.market, pair))
    return
    res = requests.get(API_URL + "markets")


if __name__ == "__main__":
    pd.options.display.width = 120
    main()
