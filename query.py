# -*- coding: utf-8 -*-
"""
"""

import os
import redis
from urllib.parse import urlparse

url = urlparse(os.environ.get("REDISCLOUD_URL"))
r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)

print(r)