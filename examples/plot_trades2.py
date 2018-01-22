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

    fig, ax1 = plt.subplots()

    ax1.plot(trades.index.to_pydatetime(), trades.price)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Price", color="b")

    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    # TODO: this should be a barchard, but does not seem to work
    ax2.plot(trades.index.to_pydatetime(), trades.amount, color="g")

    ax2.set_ylabel("Amount", color="g")
    ax2.tick_params('y', colors='g')

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
