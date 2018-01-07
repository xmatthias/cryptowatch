#!/usr/sbin/env python
from cryptowatch import CryptoMarket
import numpy as np
import matplotlib.pyplot as plt


def main():
    """
    Main Example for plot_orderbook
    """
    cm = CryptoMarket("kraken", "xrpeur")

    order_book = cm.getorderbook()
    asks = order_book["asks"]
    bids = order_book["bids"]
    bid_prices = [x["Price"] for idx, x in bids.iterrows()]
    # bid_sizes = np.cumsum([x[1] for x in order_book["bids"]])
    # bid_sizes = bids.cumsum()["Amount"].tolist()
    bid_sizes = np.cumsum(bids["Amount"])
    ask_prices = [x["Price"] for idx, x in asks.iterrows() if x["Price"] < 150]
    # ask_sizes = np.cumsum([x[1] for x in order_book["asks"] if x[0] < 150])
    # ask_sizes = asks.loc[asks["Price"] < 150].cumsum()["Amount"].tolist()
    ask_sizes = np.cumsum(asks["Amount"])

    plt.figure()
    ax = plt.gca()
    print(bid_prices)
    plt.plot(bid_prices, bid_sizes, lw=1, color='green')
    ax.fill_between(bid_prices, bid_sizes, interpolate=False, color='green')
    plt.plot(ask_prices, ask_sizes, lw=1, color='red')
    ax.fill_between(ask_prices, ask_sizes, interpolate=True, color='red')

    plt.show()

if __name__ == "__main__":
    main()
