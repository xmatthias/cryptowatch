# Cryptowat.ch API Client
This project is still a work in progress and may still have breaking changes

## usage:
```python cryptowat.py --help```

To get the latest BTC/EUR price from kraken:  
```python cryptowat.py -m kraken -p btcusd```


### usage in other scripts:

``` python
from cryptowatch import CryptoMarket
# Initialize object and print price summary 
cm = CryptoMarket("kraken", "btcusd")
print(cm)
# Refresh price in the market object:
cm.updateprice()
# Refresh summary (costs more than only price update!)
cm.updatesummary()

```


## disclaimer
I am in no way affiliated with Cryptowat.ch.
