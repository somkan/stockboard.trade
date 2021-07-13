import sys
import requests
import csv
import re
import json
import pandas as pd
import os
import pymongo
from datetime import date
fyers = None

from fyers_api import fyersModel, accessToken


def telegram(message1,message2):
    bot_message = str(message1) + str(message2)
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def get_token(app_id, app_secret, fyers_id, password, pan_dob):
    appSession = accessToken.SessionModel(app_id, app_secret)
    response = appSession.auth()
    if response["code"] != 200:
        return response
        notification("Fyers Status", response["code"])
        telegram("Fyers status",response["code"])
        # sys.exit()
    else:
        notification("Fyers Status",response["message"])
        telegram("Fyers status",response["message"])
    auth_code = response["data"]["authorization_code"]

    appSession.set_token(auth_code)

    generateTokenUrl = appSession.generate_token()
    # webbrowser.open(generateTokenUrl, new=1)
    headers = {
        "accept": "*/*",
        "accept-language": "en-IN,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json; charset=UTF-8",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referrer": generateTokenUrl
    }
    payload = {"fyers_id": fyers_id, "password": password,
               "pan_dob": pan_dob, "appId": app_id, "create_cookie": False}
    result = requests.post("https://api.fyers.in/api/v1/token",
                           headers=headers, json=payload, allow_redirects=True)
    if result.status_code != 200:
        print('error occurred status code :: ', result.status_code)
        return
    print(result.json())
    result_url = result.json()["Url"]
    token_re = re.search(r'access_token=(.*?)&', result_url, re.I)
    if token_re:
        return token_re.group(1)
    return "error"


def main():
 
    access_token = get_token(app_id=app_id, app_secret=app_secret,
                             fyers_id=fyers_id, password=password, pan_dob=pan_or_dob)

    myReq = {"fyers_id": fyers_id, "access_token": access_token}
    Access_user = {"fyers_id": userid}
    try:
        d = mycol2.delete_one(Access_user)
        x = mycol2.insert_one(myReq)
    except Exception as e:
        print(e)
    
    telegram("Fyers Access Token Generated for:",userid)
    global fyers

    token = MYCOL2.find({}, {"fyers_id", "access_token"})
    for data in token:
    	if data['fyers_id'] ==userid:
        	access_token = data['access_token']

    fyers = fyersModel.FyersModel()
    print(fyers.get_profile(token=access_token))
    print(fyers.funds(token=access_token))

if __name__ == '__main__':
    main()