from flask import Flask, request, abort, Response
import os
import json
import pymongo
from datetime import date
import requests

# 8/7/21 - Updated Strategy143
app = Flask(__name__)

myclient = pymongo.MongoClient(DBCONNECTION)
mydb = myclient[MASTERDB]
mycol2 = mydb[ACCESS_TOKEN]
myStrategy1 = mydb[STG1]
myStrategy2 = mydb[STG2]
myStrategy3 = mydb[STG3]

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
def telegram(message1,message2):
    bot_token = BOT_TOKEN # paste bot_token
    bot_chatID = MONITOR_SIGNAL  #chatid of Telegram group Monitor Signal
    bot_message = str(message1) + str(message2)+"\n"

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


@app.route('/')
def index():
    return "HI Welcome to Stockboard"

@app.route('/strategy1', methods=['POST'])
def get_webhook1():
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    if request.method == 'POST':
 #       print("received data: ", request.json)
        data = json.loads(request.data)
        ticker = data['stocks'].split(',')[0]
        price = data['trigger_prices'].split(',')[0]
        when = data['triggered_at']
        webhook_ref = data['webhook_url']
        telegram("Strategy1| ",msg)
        file_data1 = {"Date":d1,"stocks": ticker,"trigger_prices":price,"triggered_at":when,"scan":webhook_ref,"Indicator":"I","user":CLIENT1}

        x = myStrategy1.insert_one(file_data1)

        return Response(status=200)
    else:
        abort(400)


@app.route('/strategy2', methods=['POST'])
def get_webhook2():
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    if request.method == 'POST':
        #       print("received data: ", request.json)
        data = json.loads(request.data)
        ticker = data['stocks'].split(',')[0]
        price = data['trigger_prices'].split(',')[0]
        when = data['triggered_at']
        webhook_ref = data['webhook_url']
        telegram("Strategy2| ", msg)
        file_data1 = {"Date": d1, "stocks": ticker, "trigger_prices": price, "triggered_at": when, "scan": webhook_ref,
                      "Indicator": "I", "user": CLIENT1}

        x = myStrategy2.insert_one(file_data1)

        return Response(status=200)
    else:
        abort(400)


@app.route('/strategy3', methods=['POST'])
def get_webhook3():
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    if request.method == 'POST':
        #       print("received data: ", request.json)
        data = json.loads(request.data)
        ticker = data['stocks'].split(',')[0]
        price = data['trigger_prices'].split(',')[0]
        when = data['triggered_at']
        webhook_ref = data['webhook_url']
        telegram("Strategy3| ", msg)
        file_data1 = {"Date": d1, "stocks": ticker, "trigger_prices": price, "triggered_at": when, "scan": webhook_ref,
                      "Indicator": "I", "user": CLIENT1}

        x = myStrategy3.insert_one(file_data1)

        return Response(status=200)
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000)
