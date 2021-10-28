import urllib.request
import pickle
import requests
import os.path
import uuid
import random
from flask import Flask, request, render_template, \
    json, jsonify, redirect, url_for
from flask_cors import CORS

# pip install -U flask-cors

#url = "https://clientes.softpymes.com.co/public_html/backend/index.php?c=Login&v=login"
url = ""
#url = "https://www.w3schools.com/html/html_forms.asp"
#url = "https://www.google.com/"

# flask setup
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.url_map.strict_slashes = False
port = 5001
host = '0.0.0.0'
debug = True

# info to control the App
data = {
    "app": "debt_portfolio",
    "forms": {
        "conn":"/app1/form/debt_portfolio/conn",
        "downloadfile":"/app1/form/debt_portfolio/downloadfile",
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
            "t": "Test"
        }
    },
    "cache_id": uuid.uuid4()
}

def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def createListFromHTML(strhtmldecode, strElWithToStart, strElWithToEnd):
    try:
        list_el = []
        st0 = strElWithToStart
        st1 = strElWithToEnd
        list_el_search = strhtmldecode.split(st0)
        if len(list_el_search)>=2:
            list_el_search.pop(0)
            for st in list_el_search:
                strhtmldecode2 = st.split(st1)
                list_el.append(st0 + strhtmldecode2[0] + st1)
        return list_el
    except Exception as e:
        return []



def getConn(url):
    with requests.Session() as s:
        r = s.get(url)
        #data = {"user[login]":"790", "user[password]":"Cl21#9150", "authenticity_token":"yfNk9+0khhVcnqtZLJLJr54erKX3UOR+4BeWL+DjfUq4l2ZgAlErFqIWhHjcXOgHbFiRQ692ZgiWjCSI4mFOSg==" }
        #r = s.post(url, data=data)
        #print(r.text)
        #print(s.cookies)
        #print(s.headers)
        #print(r.encoding) #ex. print: utf-8
        #Use .content to access the byte stream, or .text to access the decoded Unicode stream.
        return r.text

def readUrlWithUtf8(url):
    try:
        with requests.Session() as s:
            r = s.get(url)
            #print(s.cookies)
            #Use .content to access the byte stream, or .text to access the decoded Unicode stream.
            return r.text
    except Exception as e:
        return ""


def readUrlWithUtf8Old(url):
    try:
        strhtmldecode = ""
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        strhtmldecode = mybytes.decode("utf8")
        fp.close()
        return strhtmldecode
    except Exception as e:
        return ""


def readFormsFromStr(strhtmldecode):
    try:
        return createListFromHTML(strhtmldecode, "<form", "</form>")
    except Exception as e:
        return []

def readAttrOfForm(strhtmldecode):
    try:
        # Is not taken into account the close with />
        return createListFromHTML(strhtmldecode, "<form", ">")
    except Exception as e:
        return []

def readInputsFromForm(strhtmldecode):
    try:
        # Is not taken into account the close with />
        return createListFromHTML(strhtmldecode, "<input", ">")
    except Exception as e:
        return []

def addNewFormJson():
    return {"uuid": str(uuid.uuid4()),"attr":{},"currEl":[]}

def addHeaderToForm(formJson, st):
    listAttrAllowed = ["method","action","enctype"]
    # find into form input tag
    formChildJson = readAttrOfForm(st)
    #print(formChildJson)
    # find elements and pass into formJson
    for currEl in formChildJson:
        formJson["attr"] = htmlToJsonFormTags(currEl, listAttrAllowed)
    return formJson

def addChildNodeToForm(formJson, st):
    listAttrAllowed = ["type","name","value","title","placeholder"]
    # find into form input tag
    formChildJson = readInputsFromForm(st)
    # find elements and pass into formJson
    for currEl in formChildJson:
        formJson["currEl"].append(htmlToJsonFormTags(currEl, listAttrAllowed))
    return formJson

# the next funciton support only attributes type String,
# ex. name="anything", class="myXclass", value="1"
def htmlToJsonFormTags(st, listAttrAllowed):
    p1 = str(st);
    childAttr = []
    childAttrJson = {}
    if p1.find('=\"')>-1:
        p2 = p1.split('=\"')
        #print(p1)
        for l1 in p2:
            p0 = l1.rfind(" ")
            tmp = l1[:p0]
            tmp = tmp[:tmp.find('\"')]
            childAttr.append(tmp)
            tmp = l1[p0 + 1:]
            tmp = tmp[:-1] if tmp.find(">") > -1 else tmp[:]
            childAttr.append(tmp)
        childAttr.pop(0)
        i = 0
        while i < len(childAttr):
            key = childAttr[i]
            value = childAttr[i+1] if i+2 < len(childAttr) else ""
            if key in listAttrAllowed:
                childAttrJson.update({key:value})
            i += 2
    return childAttrJson


@app.route('/api/v1/settingConn', methods=['POST'])
def settingConn():
    try:
        _request = request.get_json(force=True)
        formJson = {}
        data["cache_id"] = _request["key"]
        url=_request["toUrl"]
        #create all forms from URL
        forms = readFormsFromStr(readUrlWithUtf8(url))
        if len(forms) == 1:
            formJson = addChildNodeToForm(addHeaderToForm(addNewFormJson(), forms[0]), forms[0])
            formJson.update({"status":"OK"})
        elif len(forms)>2:
            formJson.update({"status":"This current version of App not support multi forms, contact your Developer"})
        else:
            formJson.update({"status":"Not detected form, review your URL"})
        #return formJson
        formJson.update({"uuid":data["cache_id"]})
        formJson.update({"toUrl":url})
        return render_template("connection.html", data=data, formJson=formJson)
    except Exception as e:
        return "Error: {}".format(str(e))


@app.route('/')
def index():
    return "Welcome, build your automation!"


if __name__ == '__main__':
    app.run(debug=debug, threaded=True, host=host, port=port)
#step: get json form,
#step: update value of json form,
#step: get last json form,
#step: get url and send credential,
#step: get url resource  and save file,
