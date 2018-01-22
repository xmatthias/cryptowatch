#!/usr/sbin/env python
from cryptowatch import CryptoMarket
import numpy as np
import matplotlib.pyplot as plt


def main():
    """
    Main Example for plot_orderbook
    """
    market = "kraken"
    pair = "xrpeur"
    cm = CryptoMarket(market, pair)

    # get Orderbook
    trades = cm.getTrades()
    print(trades)

    plt.figure(figsize=(10, 5))
    top = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)

    bottom = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)

    top.plot(trades.index.to_pydatetime(), trades.price)
    bottom.bar(trades.index.to_pydatetime(), trades.amount, color="blue")

    top.axes.get_xaxis().set_visible(False)
    top.set_title(market + " last trades")
    top.set_ylabel('Price')

    bottom.set_ylabel('Volume')

    plt.show()


if __name__ == "__main__":
    main()
