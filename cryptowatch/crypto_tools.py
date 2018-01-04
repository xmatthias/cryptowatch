"""general Tools for cryptowatch - cannot be used independently"""
import json
from collections import namedtuple

import requests
from colorama import Fore

VERBOSE = False
API_URL = "https://api.cryptowat.ch/"

allowance = {}
PROXY = {}

MAXALLOWANCE = 8000000000
# 8s


# source: https://stackoverflow.com/questions/
# 6578986/how-to-convert-json-data-into-a-python-object
def _json_object_hook(dat):
    """Json hook to convert json object to named tuple
    DO NOT CALL DIRECTLY"""
    return namedtuple('X', dat.keys())(*dat.values())


def json2obj(data):
    """Convert json object to NamedTuple"""
    return json.loads(data, object_hook=_json_object_hook)


def request(url, convert=True):
    """Requests to api and return python object"""
    # pylint: disable=W0603
    global allowance
    req = requests.get(url, proxies=PROXY)
    if convert:
        res = json2obj(req.text)

        allowance = res.allowance
        res = res.result
    else:
        allowance = json2obj(json.dumps(req.json()["allowance"]))
        res = req.json()["result"]

    printallowance()
    return res


def printallowance():
    """prints remaining allowance"""
    rem = int(allowance.remaining)
    cost = int(allowance.cost)
    avg_rem = rem / cost
    perc = rem / MAXALLOWANCE * 100
    if VERBOSE:
        print(Fore.YELLOW + "Allowance:" + Fore.LIGHTWHITE_EX)
        print("Cost:", cost)
        print("Remaining:", rem)
        print("AvgRemReq:", avg_rem)
        print("PercRem:", perc, "%")
        print()
