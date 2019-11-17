import os

from flask import Flask

for i in os.listdir("/home/ateryohin/workspace/python/mail_cv/app/static/upload"):
    os.remove(f"/home/ateryohin/workspace/python/mail_cv/app/static/upload/{i}")

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
from . import view