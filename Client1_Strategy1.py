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

myclient =app.config.get("DBCONNECTION")
mydb = app.config.get("MASTERDB")
mycol = app.config.get("AUTH_DATA")
mycol2 = app.config.get("ACCESS_TOKEN")
strategy1 = app.config.get("STG1")
userid = app.config.get("CLIENT1")


global fyers,capital,allot
token = mycol2.find({}, {"fyers_id", "access_token"})
# is_async = False #(By default False, Change to True for asnyc API calls.)


def telegram(message1,message2):
    bot_token = app.config.get("BOT_TOKEN")  # paste bot_token
    bot_chatID = app.config.get("MONTOR_SIGNAL")  # paste your chatid where you want to send alert(group or channel or personal)
    bot_message = str(message1) + str(message2)
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def main(quantity,ticker,price1):
        try:
            trade=fyers.place_orders(
            token=access_token,
            data = {
            "symbol": ticker,
            "qty": quantity,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": price1,
            "stopPrice": 0,
            "disclosedQty": 0,
            "validity": "Day",
            "offlineOrder": "True",
            "stopLoss": 0,
            "takeProfit": 0
            }
            )
            stat=trade["message"]
            #print(stat)
            message(userid,stat)
            #print("stock :"+ticker,"quantity:"+str(quantity),"Price:"+str(price1))
            msg1 = "stock :"+ticker,"quantity:"+str(quantity),"Price:"+str(price1)
            telegram(msg1,stat)
        except Exception as e:
#            print("API error for ticker :",e)
            telegram("API error for ticker :",e)
            exit()
#############################################################################################################
#############################################################################################################
for data in token:
    if data['fyers_id'] ==userid:
        access_token = data['access_token']

fyers = fyersModel.FyersModel()
#print(access_token)
try:
    portfolio=fyers.funds(token=access_token)
    #print(portfolio)
    # get the equityAmount from the response and add % to capital allotment
    if portfolio["code"] !=401:
        fund = portfolio["data"]["fund_limit"][0]
        allot=fund["equityAmount"]
        capital = int(float(allot))  # 100% funds allocated to this strategy
        #print(capital)
        capital = int(capital)
    else:
        telegram(portfolio["code"],portfolio["message"])
except Exception as w:
    #print(w)
starttime=time.time()
telegram("Good Morning", "Stockboard.trade -Strategy1 running")
timeout = time.time() + 60*60*6  # 60 seconds times 360 meaning 6 hrs
while time.time() <= timeout:
    try:
        key_signal = strategy1.find({}, {"stocks", "trigger_prices", "user", "Indicator"})
        for data in key_signal:
            if data["user"] == userid:
                if data["Indicator"] == "I":
                    strategy1_ticker = data['stocks']
                    strategy1_price = data['trigger_prices']
                    strategy1.update_one(
                        {"user": userid},
                        {'$set': {"Indicator": "C"}}
                    )
                    msg = "Signal picked for " + userid
                    telegram(msg, " Flag Changed")
                    ticker = "NSE:" + strategy1_ticker +"-EQ"
                    price1 = strategy1_price
                    price1 = (int(float(price1)))
                    quantity = (capital // price1) * 7
                    main(quantity, ticker, price1)
                    time.sleep(60 - ((time.time() - starttime) % 60.0))
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        telegram("User Stopped for: ",userid)
        exit()