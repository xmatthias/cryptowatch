#!/usr/sbin/env python3
import argparse

import pandas as pd
# from pandas.io.json import json_normalize

import crypto_info as ci
import crypto_market as cm


def main():
    """main method - mainly argparser calling other functions"""
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

    parser.add_argument("--orderbook", dest="orderbook", action="store_true",
                        help="print orderbook TODO: complete printing")

    parser.add_argument("--ohlc", dest="ohlc", action="store_true",
                        help="get OHLC Candlestick data")

    parser.add_argument("--getallprices", dest="getallprices",
                        action="store_true", required=False,
                        help="Get all prices exit")
    args = parser.parse_args()

    if args.listassets:
        ci.printassets(ci.listassets())
        return

    if args.asset:
        ci.printasset(ci.getasset(args.asset))

    if args.listpairs:
        ci.printpairs(ci.listpairs())

    if args.getpair:
        ci.printpair(ci.getpair(args.getpair))

    if args.listexchanges:
        ci.printexchanges(ci.listexchanges())
        return

    if args.listmarkets:
        ci.printmarkets(ci.listmarkets())

    if args.market and not args.pairs:
        markets = ci.listmarkets(args.market)
        ci.printmarkets(markets)
        return

    if args.market and args.pairs and args.orderbook:
        for pair in args.pairs:
            print(cm.getorderbook(args.market, pair))
        return

    if args.market and args.pairs and args.ohlc:
        for pair in args.pairs:
            print(cm.getohlc(args.market, pair))
        return

    if args.market and args.pairs:
        for pair in args.pairs:
            print(cm.getmarketpair(args.market, pair))

    if args.getallprices:
        ci.printprices(ci.getallprices())

if __name__ == "__main__":
    pd.options.display.width = 120
    main()
