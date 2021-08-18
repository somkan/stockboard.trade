from flask import Flask, request, abort, Response,render_template
import os
import json
import pymongo
from datetime import date
import requests

# 8/7/21 - Updated Strategy143
app = Flask(__name__)
DBCONNECTION = app.config.get("DBCONNECTION")
MASTERDB = app.config.get("MASTERDB")
ACCESS_TOKEN = app.config.get("ACCESS_TOKEN")
AUTH_USER = app.config.get("AUTH_USER")
STG1 = app.config.get("STG1")
STG2 = app.config.get("STG2")
STG3 = app.config.get("STG3")
STG4 = app.config.get("STG4")

myclient = DBCONNECTION
mydb = MASTERDB
mycol2 = ACCESS_TOKEN
myStrategy1 = STG1
myStrategy2 = STG2
myStrategy3 = STG3
myTrade = STG4
myAuth = AUTH_USER

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
def telegram(message1,message2):
    BOT_TOKEN = app.config.get(BOT_TOKEN)
    MONITOR_SIGNAL = app.config.get(MONITOR_SIGNAL)

    bot_token = BOT_TOKEN # paste bot_token
    bot_chatID = MONITOR_SIGNAL  #chatid of Telegram group Monitor Signal
    bot_message = str(message1) + str(message2)+"\n"

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def response():
 fname = request.form.get("fname")
 passwd = request.form.get("passwd")
 key_data = myAuth.find({}, {"uname", "passwd"})
 for record in key_data:
    uname = record["uname"]
    if uname == fname and passwd == record["passwd"]:
        fname = uname
        return render_template("login.html", name=fname)
    else:
        fname = "Unknown User"
        return render_template("index.html", name=fname)

@app.route('/cpr1', methods=['POST'])
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
        telegram("Stockboard-Alert-Heroku| ", msg)
        file_data1 = {"Date": d1, "stocks": ticker, "trigger_prices": price, "triggered_at": when, "scan": webhook_ref,
                      "Indicator": "I", "user": CLIENT1}

        x = myTrade.insert_one(file_data1)

        return Response(status=200)
    else:
        abort(400)

if __name__ == '__main__':
    telegram("Stockboard APP","Running in Heroku")
    app.run()