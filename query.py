# -*- coding: utf-8 -*-
"""
"""

import os
import pymongo

myClient =str(os.environ.get("DBCONNECTION"))
mydb = str(os.environ.get("MASTERDB"))
strategy1 =str(os.environ.get("STG1"))
userid = os.environ.get("CLIENT1")
print(mydb)
print(strategy1)
print(userid)
key_signal = strategy1.find({"user":userid}, {"stocks", "trigger_prices", "user", "Indicator"})
key_sign = strategy1.find({})
#key_signal = strategy1.find({})
for data in key_signal:
    print(data["user"])