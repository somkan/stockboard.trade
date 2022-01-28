# -*- coding: utf-8 -*-
"""
"""
from fyers_api import fyersModel, accessToken
import json
import os
import datetime as dt
import time
import requests
from datetime import datetime
import pymongo
from datetime import date
import logging
import os

myclient =os.environ.get("DBCONNECTION")
myclient1=myclient
mydb = myclient1["StockboardDB"]
#strategy1 = os.environ.get("STG1")
strategy1 =mydb["strategy1"]
userid = os.environ.get("CLIENT1")
print(mydb)
print(strategy1)
print(userid)
key_signal = strategy1.find({}, {"stocks", "trigger_prices", "user", "Indicator"})
#key_signal = strategy1.find({})
for data in key_signal:
    print(data["user"])