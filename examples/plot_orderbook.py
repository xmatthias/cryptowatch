#!/usr/sbin/env python
from cryptowatch import CryptoMarket
import numpy as np
import matplotlib.pyplot as plt


def main():
    """
    Main Example for plot_orderbook
    """
    cm = CryptoMarket("kraken", "xrpeur")

    # get Orderbook
    order_book = cm.getorderbook()

    asks = order_book["asks"]
    bids = order_book["bids"]

    # get cumulative sums
    bid_sizes = np.cumsum(bids["Amount"])
    ask_sizes = np.cumsum(asks["Amount"])

    plt.figure()
    ax = plt.gca()

    plt.axvline(x=cm.price)
    ax.annotate('Curr.Price ' + str(cm.price), xy=(cm.price, 1),
                xytext=(cm.price * 0.96, 1),
                arrowprops=dict(facecolor='black', shrink=0.05),
                )

    plt.plot(bids["Price"], bid_sizes, lw=1, color='green')
    ax.fill_between(bids["Price"], bid_sizes, interpolate=False,
                    color='#00FF0088')
    plt.plot(asks["Price"], ask_sizes, lw=1, color='red')
    ax.fill_between(asks["Price"], ask_sizes,
                    interpolate=True, color='#FF000088')

    # Vertical plot
    # plt.plot(bid_sizes, bids["Price"], lw=1, color='green')
    # ax.fill_betweenx(bids["Price"], bid_sizes, interpolate=True,
    #                  color='green')
    # plt.plot(ask_sizes, asks["Price"], lw=1, color='red')
    # ax.fill_betweenx(asks["Price"], ask_sizes, interpolate=True, color='red')

    plt.show()

if __name__ == "__main__":
    main()
