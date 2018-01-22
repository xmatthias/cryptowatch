"""CryptoMarket class module"""
from cryptowatch.crypto_tools import request, API_URL
import pandas as pd


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

    def __init__(self, exchange, currencypair, empty=False):
        """
        initialize market class (and get summary!)
        exchange:       Exchange
        currencypair:   sample: [btcusd]
        empty:          don't run any call to cryptowat.ch on initialisation
                        in order to save API Requests
        """
        self.exchange = exchange
        self.pair = currencypair
        if not empty:
            self.updatesummary()

    def __str__(self):
        return (f'Pair: {self.pair} '
                f'last: {self.price} high: {self.highprice} '
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
        returns a Dictionary with bids / asks in Panda Dataframes.
        details:
        https://cryptowat.ch/docs/api#orderbook
        """
        columns = ["Price", "Amount"]
        orb = request(API_URL + "markets/" + self.exchange + "/" +
                      self.pair + "/orderbook", False)
        asks = pd.DataFrame(orb["asks"], columns=columns)
        bids = pd.DataFrame(orb["bids"], columns=columns)
        print("asks:", len(asks), "bids:", len(bids))
        return {"asks": asks, "bids": bids}

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

    def getTrades(self):
        """
        get's latest trade data as Panda DataFrame
        details:
        https://cryptowat.ch/docs/api#trades
        """
        columns = ["id", "timestamp", "price", "amount"]
        trades = request(API_URL + "markets/" + self.exchange + "/" +
                         self.pair + "/trades")
        df = pd.DataFrame(trades, columns=columns)
        df.timestamp = pd.to_datetime(df.timestamp, unit="s")
        df.set_index("timestamp",  inplace=True)

        df.drop("id", axis=1, inplace=True)
        return df
