import urllib.request
import requests
import os.path
import uuid
import random
import json
import pickle

################################################################
########################## create session for service ##########
################################################################
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


def readUrlWithUtf8Pro(url):
    try:
        with requests.Session() as s:
            #headers = requests.utils.default_headers()
            #headers.update({'User-Agent': 'Mozilla/5.0'})
            s.headers.update({'User-Agent': 'Mozilla/5.0'})
            #print(s.cookies)
            #debug = {'verbose': sys.stderr}
            r = s.get(url)
            #print(s.cookies)
            with open("static/files/cookie", 'wb') as f:
                serial_cookies = pickle.dumps( s.cookies )
                f.write(serial_cookies)
                f.close()
            print("readUrlWithUtf8 >>")
            print(s.headers)
            print(s.cookies)
            print("<< readUrlWithUtf8")
            #Use .content to access the byte stream, or .text to access the decoded Unicode stream.
            return {"s":s, "r":r}
    except Exception as e:
        return ""

def readUrlWithUtf8(url):
    try:
        with requests.Session() as s:
            #headers = requests.utils.default_headers()
            #headers.update({'User-Agent': 'Mozilla/5.0'})
            s.headers.update({'User-Agent': 'Mozilla/5.0'})
            #print(s.cookies)
            #debug = {'verbose': sys.stderr}
            r = s.get(url)
            #print(s.cookies)
            with open("static/files/cookie", 'wb') as f:
                serial_cookies = pickle.dumps( s.cookies )
                f.write(serial_cookies)
                f.close()
            print("readUrlWithUtf8 >>")
            print(s.headers)
            print(s.cookies)
            print("<< readUrlWithUtf8")
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
################################################################
########################## create session for service end ######
################################################################

################################################################
########################## read html and print forms ###########
################################################################
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

# add data to json with all attributes of form
def addHeaderToForm(formJson, st):
    listAttrAllowed = ["method","action","enctype"]
    # find into form input tag
    formChildJson = readAttrOfForm(st)
    #print(formChildJson)
    # find elements and pass into formJson
    for currEl in formChildJson:
        formJson["attr"] = htmlToJsonFormTags(currEl, listAttrAllowed)
    return formJson

# add data to json with all elements of form
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
