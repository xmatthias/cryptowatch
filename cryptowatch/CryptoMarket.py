"""CryptoMarket class module"""
from cryptowatch.crypto_tools import request, API_URL


class CryptoMarket:
    """
    Market class to interface with cryptowat.ch API
    * Price
    * highprice
    * lowprice
    * volume
    * change
    """
    price = float
    highprice = float
    lowprice = float
    volume = float
    changeperc = float
    changeabs = float
    exchange = str
    pair = str

    def __init__(self, exchange, currencypair):
        """
        initialize market class (and get summary!)
        exchange: Exchange
        currencypair: sample: [btcusd]
        """
        self.exchange = exchange
        self.pair = currencypair
        self.updatesummary()

    def __str__(self):
        return (f'last: {self.price} high: {self.highprice} '
                f'low: {self.lowprice} '
                f'volume: {self.volume}\t'
                f'changeperc: {self.changeperc} '
                f'changeabs: {self.changeabs}')

    def updateprice(self):
        """Updates price"""
        json = request(API_URL + "markets/" + self.exchange + "/" +
                       self.pair + "/price", False)
        self.price = json["price"]

    def updatesummary(self):
        """Updates Summary (price, high, low, change) for this Market"""
        pair = request(API_URL + "markets/" + self.exchange + "/" +
                       self.pair + "/summary", False)
        self.price = pair["price"]["last"]
        self.highprice = pair["price"]["high"]
        self.lowprice = pair["price"]["low"]
        self.volume = pair["volume"]
        self.changeabs = pair["price"]["change"]["absolute"]
        self.changeperc = pair["price"]["change"]["percentage"]

    def getorderbook(self):
        """
        get's orderbook for the selected exchange/pair combination
        Access using result.bids and result.asks
        details:
        https://cryptowat.ch/docs/api#orderbook
        """
        orb = request(API_URL + "markets/" + self.exchange + "/" +
                      self.pair + "/orderbook")
        print("asks:", len(orb.asks), "bids:", len(orb.bids))
        return orb

    def getohlc(self, ohlclimit):
        """
        get's ohlc (candle stick data) for the selected
        exchange/pair combination
        details:
        https://cryptowat.ch/docs/api#ohlc
        """
        args = ""
        if ohlclimit:
            args += "periods=" + ohlclimit
        ohlc = request(API_URL + "markets/" + self.exchange + "/" +
                       self.pair + "/ohlc?" + args,
                       False)
        return ohlc
