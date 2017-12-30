from crypto_tools import request, API_URL


def printmarketsummary(pair):
    print(f'last: {pair.price.last} high: {pair.price.high} '
          f'low: {pair.price.low} '
          f'volume: {pair.volume}')


def getmarketpair(exchange, pair):
    """Get's pairs for the selected exchange / pair combinations"""
    pair = request(API_URL + "markets/" + exchange + "/" + pair + "/summary")
    return pair


def getorderbook(exchange, pair):
    """get's orderbook for the selected exchange/pair combination"""
    ord = request(API_URL + "markets/" + exchange + "/" + pair + "/orderbook")
    print("asks:", len(ord.asks), "bids:", len(ord.bids))
    return ord


def getohlc(exchange, pair):
    """get's ohlc (candle stick data) for the selected
    exchange/pair combination"""
    ohlc = request(API_URL + "markets/" + exchange + "/" + pair + "/ohlc",
                   False)
    return ohlc
