import os
import redis
from urllib.parse import urlparse
import json
from flask import Flask, request, abort, Response, render_template,jsonify
from redis.commands.json.path import Path

app = Flask(__name__)

url = urlparse(os.environ.get("REDISCLOUD_URL"))
client = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True,
                     ssl_cert_reqs=None)

@app.route('/strategy9', methods=['GET'])
def get_respond():
    data = request.args.get("stocks",None)
    print("got stock {stocks}")
    response = {}
    response["MESSAGE"] = "Buy {stocks}"
    return jsonify(response)


@app.route('/strategy9', methods=['POST'])
def get_webhook1():
    data = json.loads(request.data)

    client.json().set('strategy:1',Path.rootPath(),data)
    result = client.json().get('strategy:1',Path('.stocks'))
    print(result)


if __name__ == '__main__':
    #telegram("Stockboard Webhook ","Running")
    app.run()