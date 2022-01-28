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

myclient =app.config.get("DBCONNECTION")
mydb = app.config.get("MASTERDB")
strategy1 = app.config.get("STG1")
userid = app.config.get("CLIENT1")

key_signal = strategy1.find({}, {"stocks", "trigger_prices", "user", "Indicator"})
for data in key_signal:
    if data["user"] == userid:
        console.log("userid")
        console.log(data["user"])