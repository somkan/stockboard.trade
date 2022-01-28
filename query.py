# -*- coding: utf-8 -*-
"""
"""

import os
import pymongo

myclient =os.environ.get("DBCONNECTION")
mydb = myclient["StockboardDB"]
strategy1 =mydb["strategy1"]
userid = os.environ.get("CLIENT1")
print(mydb)
print(strategy1)
print(userid)
key_signal = strategy1.find({}, {"stocks", "trigger_prices", "user", "Indicator"})
#key_signal = strategy1.find({})
for data in key_signal:
    print(data["user"])