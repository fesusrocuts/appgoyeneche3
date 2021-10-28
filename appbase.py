import urllib.request
#import pickle
import requests
import os.path
import uuid
import random
from flask import Flask, request, render_template, \
    json, jsonify, redirect, url_for
from flask_cors import CORS

################################################################
########################## flask setup #########################
################################################################
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'
debug = True
################################################################
########################## flask setup end #####################
################################################################


# https://clientes.softpymes.com.co/public_html/backend/index.php?c=Login&v=login
# usuario
# password
# method=POST
# https://github.com/fesusrocuts/appgoyeneche1/raw/master/2019-11-26%20Cartera.xls

#fesusrocuts@gmail.com
#https://github.com/login?return_to=%2Ffesusrocuts%2Fappgoyeneche1
#https://github.com/fesusrocuts/appgoyeneche1


################################################################
########################## json setup ##########################
################################################################
data = {
    "app": "debt_portfolio",
    "forms": {
        "conn":"/app1/form/debt_portfolio/conn",
        "send":"/app1/form/debt_portfolio/send",
        "downloadfile":"/app1/form/debt_portfolio/downloadfile",
        "uploadfile":"/app1/form/debt_portfolio/uploadfile",
        "notifications":"/app1/form/debt_portfolio/notifications",
        "templates":"/app1/form/debt_portfolio/templates",
        "building":"/app1/form/debt_portfolio/building",
    },
    "labels": {
        "title": "Service for building Automated Actions - Beta FR",
        "msg_welcome": "Welcome, build your automation!",
        "author": "By Fesus Rocuts",
        "authorurl": "https://www.linkedin.com/in/fesus/",
        "btns": {
            "c": "create",
            "r": "read",
            "u": "update",
            "d": "delete",
            "s": "save",
            "c2": "continue",
            "a": "Add",
            "t": "Test",
            "f": "Finalize",
            "sm": "Send message"
        }
    },
    "cache_id": uuid.uuid4()
}
################################################################
########################## json setup end ######################
################################################################


################################################################
########################## default url of service ##############
################################################################
@app.route('/')
def index():
    return render_template("index.html", data=data)

################################################################
########################## default url of service ##############
################################################################
@app.route('/sendNotification')
def sendNotification():
    return render_template("sendNotification.html", data=data)
