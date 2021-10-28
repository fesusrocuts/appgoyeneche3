import requests
import os, sys
from random import randint
import uuid
from formFromUrl import *
from appbase import app
from appbase import *
import json
import time
from appfirebase import *
from appexcel import *
from flask import Flask, render_template, request, abort, jsonify
from werkzeug import secure_filename

################################################################
########################## form to service #####################
################################################################
@app.route('/app1/form/debt_portfolio/file', methods=['GET', 'POST', 'PUT', 'DELETE'])
def form_upfile():
    #_request = request.get_json(force=True)
    if request.method == 'POST':
        f = request.files['file']
        f.save("static/files/{}".format(secure_filename("current.xls")))
        return 'file debtors uploaded successfully'
    return render_template("file.html", data={})

@app.route('/app1/form/debt_portfolio/file2', methods=['GET', 'POST', 'PUT', 'DELETE'])
def form_upfile2():
    #_request = request.get_json(force=True)
    if request.method == 'POST':
        f = request.files['file']
        f.save("static/files/{}".format(secure_filename("clients.xls")))
        try:
            os.remove("static/files/clients.json")
        except Exception as e:
            pass
        return 'file clients uploaded successfully'
    return render_template("file2.html", data={})


@app.route('/app1/form/debt_portfolio/conn', methods=['GET', 'POST', 'PUT', 'DELETE'])
def form_conn():
    _request = request.get_json(force=True)
    register2 = {}
    dataForm =  _request.get("data")
    data["cache_id"] = _request["key"]

    if(dataForm is not None):
        for item in dataForm:
            register2.update({item.get("name"): item.get("value")})
        register2.update({"__message": []})
        register = {_request["key"]:register2}
        ##########################
        print("add data collection .....")
        doc_ref = db.collection(u'process1').document(u'{}'.format(_request["key"]))
        doc_ref.set(register2)
        print("add data collection end .....")
        ##########################
        print("select data collection .....")
        collection_ref = db.collection(u'process1')
        docs = collection_ref.stream()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
        print("select data collection end .....")
        ##########################
        return {"status":"ok","register":register}
        #return redirect(url_for('/app1/form/debt_portfolio/downloadfile'))
    else:
        return render_template("conn.html", data=data)

@app.route('/app1/form/debt_portfolio/downloadfile', methods=['GET', 'POST', 'PUT', 'DELETE'])
def form_downloadfile():
    _request = request.get_json(force=True)
    register2 = {}
    dataForm =  _request.get("data")
    data["cache_id"] = _request["key"]

    if(dataForm is not None):
        for item in dataForm:
            register2.update({item.get("name"): item.get("value")})
        #register2.update({"__message": []})
        register = {_request["key"]:register2}
        ##########################
        print("add data collection .....")
        doc_ref = db.collection(u'process1').document(u'{}'.format(_request["key"]))
        doc_ref.update(register2)
        print("add data collection end .....")
        ##########################
        """
        print("select data collection .....")
        collection_ref = db.collection(u'process1')
        docs = collection_ref.stream()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
        print("select data collection end .....")
        """
        ##########################
        return {"status":"ok","register":register}
        #return redirect(url_for('/app1/form/debt_portfolio/downloadfile'))
    else:
        return render_template("downloadfile.html", data=data)


def getFileQueue(filename = '', path = 'static/files/queue/'):
    # Give the location of the file, is relative
    file = '{}{}{}'.format(path,filename,".json")
    if os.path.exists(file) is False:
        raise NameError('FileNotFoundError')
    return file;

@app.route('/app1/form/debt_portfolio/sendQueue/<string:q>/', methods=['GET'])
def sendQueue(q):
    #_request = request.get_json(force=True)
    #_q = request.args.get("q", "")
    try:
        queue = getFileQueue(q)
        data2 = load_from_json_file(queue)
        #data["cache_id"] = str(uuid.uuid4())
        #data["status"] = "Ok"
        #return jsonify(status=202)
        data2.update({"sendmail":False})
        if "notification" in data2.keys():
            if "to" in data2.get("notification").keys():
                try:
                    try:
                        sendmailhtml("contabilidad@comercializadoragyl.com", data2.get("notification").get("to"), "{}".format(data2.get("notification").get("subject")), 'Hi, The next message you see correctly with html format',data2.get("notification").get("message"))
                        data2.update({"sendmail":True})
                    except Exception as e:
                        data2.update({"sendmail_to_err":str(e)})
                        data2.update({"sendmail_to_errm":str(e.message)})
                        data2.update({"sendmail_to_errc":str(e.code)})

                    try:
                        sendmailhtml("contabilidad@comercializadoragyl.com", data2.get("notification").get("cc"), "cc. {}".format(data2.get("notification").get("subject")), 'Hi, The next message you see correctly with html format',data2.get("notification").get("message"))
                    except Exception as e:
                        data2.update({"sendmail_cc_err":str(e)})
                        data2.update({"sendmail_cc_errm":str(e.message)})
                        data2.update({"sendmail_cc_errc":str(e.code)})

                    try:
                        sendmailhtml("contabilidad@comercializadoragyl.com", data2.get("notification").get("bcc"), "bcc. {}".format(data2.get("notification").get("subject")), 'Hi, The next message you see correctly with html format',data2.get("notification").get("message"))
                    except Exception as e:
                        data2.update({"sendmail_bcc_err":str(e)})
                        data2.update({"sendmail_bcc_errm":str(e.message)})
                        data2.update({"sendmail_bcc_errc":str(e.code)})

                except Exception as e:
                    pass
        #return jsonify(data2.get("status")), 200
        #return render_template("sendQueueLog.html", data=data2)
        try:
            data2.get("client").pop("values",None)
        except Exception as e:
            pass

        try:
            os.remove(queue)
        except Exception as e:
            pass

        return data2, 200
    except Exception as e:
        return abort(404, "Resource not found")
        #return jsonify({"status":"Not exist file"}), 404


@app.route('/app1/form/debt_portfolio/send', methods=['GET', 'POST', 'PUT', 'DELETE'])
def form_notifications():
    print("form_notifications >>>>>>>>>>>>>>>>")
    try:
        _request = request.get_json(force=True)
        data["cache_id"] = _request["key"]
    except Exception as e:
        data["cache_id"] = uuid.uuid4()

    try:
        readFileXlsClients(getFileClients())
        readFileXls(getFile())
        queue = load_from_json_file("static/files/queue.json")
        #updateStatusQueue()
    except Exception as e:
        print(e)
        return render_template("sendQueueLog.html", data={"msgerr":"File not found"})
    
    try:
        os.remove("static/files/queue.json")
    except Exception as e:
        pass


    print("form_notifications >> queue >>")
    print(queue)
    print("<< form_notifications << queue")
    # time.sleep(10)
    data.update({"status":"OK"})
    data.update({"queue":queue})
    data.update({"cache_id":str(uuid.uuid4())})
    if len(queue)>0:
        data.update({"message":"It was created one file to send mail, please wait while file is process, please don't close the current window until below into box show otherwise."})
    else:
        data.update({"message":"Apparently the debt portfolio is clean, you can close the current window."})
    return render_template("sendNotification2.html", data=data)
    #return data

@app.route('/app1/form/debt_portfolio/building', methods=['GET', 'POST', 'PUT', 'DELETE'])
def form_building():
    _request = request.get_json(force=True)
    currentdata = {}
    doc_ref = db.collection(u'process1')
    docs = doc_ref.stream()
    for doc in docs:
        if _request["key"] == doc.id:
            currentdata = doc.to_dict()
    save_to_json_file(currentdata, "static/files/setting.json")
    return render_template("building.html", data={"status":"ok","message":"Successfully save your configuration, the system get this info to download file, browse the file and send mail."})
    #return {"status":"ok","message":"Sucessfully save your configuration, the system get this info to download file, browse the file and send mail."}

@app.route('/app1/form/debt_portfolio/templates', methods=['GET', 'POST', 'PUT', 'DELETE'])
def form_templates():
    _request = request.get_json(force=True)
    register2 = {}
    dataForm =  _request.get("data")
    data["cache_id"] = _request["key"]
    data["formid"] = "new" #str(uuid.uuid4())
    if(dataForm is not None):
        for item in dataForm:
            if item.get("name") =="id" and item.get("value") == "new":
                register2.update({"id": str(uuid.uuid4())})
            else:
                register2.update({item.get("name"): item.get("value")})

        print("register2 >> ")
        print(register2)
        print("<< register2")
        #register = {"__message":[register2]}
        ##########################
        print("add data collection .....")
        doc_ref = db.collection(u'process1')
        doc_ref2 = db.collection(u'process1').document(u'{}'.format(_request["key"]))
        docs = doc_ref.stream()
        for doc in docs:
            if _request["key"] == doc.id:
                currentdata = doc.to_dict()
                __message = currentdata.get("__message")
                __message.append(register2)

        doc_ref2.update({"__message":__message})
        print("add data collection end .....")
        ##########################
        """
        print("select data collection .....")
        collection_ref = db.collection(u'process1')
        docs = collection_ref.stream()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
        print("select data collection end .....")
        """
        ##########################
        return {"status":"ok","message":__message}
        #return redirect(url_for('/app1/form/debt_portfolio/downloadfile'))
    else:
        return render_template("templates.html", data=data)

################################################################
########################## form to service end #####################
################################################################

################################################################
########################## read html and print forms ###########
################################################################
# fn to create forms form others servers
@app.route('/api/v1/settingConn', methods=['POST'])
def settingConn():
    try:
        _request = request.get_json(force=True)
        formJson = {}
        data["cache_id"] = _request["key"]
        __toUrl=_request["__toUrl"]
        __toEmail=_request["__toEmail"]
        #create all forms from URL
        forms = readFormsFromStr(readUrlWithUtf8(__toUrl))
        if len(forms) == 1:
            formJson = addChildNodeToForm(addHeaderToForm(addNewFormJson(), forms[0]), forms[0])
            formJson.update({"status":"OK"})
        elif len(forms)>2:
            formJson.update({"status":"This current version of App not support multi forms, contact your Developer"})
        else:
            formJson.update({"status":"Not detected form, review your URL"})
        #return formJson
        formJson.update({"uuid":data["cache_id"]})
        formJson.update({"__toUrl":__toUrl})
        formJson.update({"__toEmail":__toEmail})
        return render_template("api_connection.html", data=data, formJson=formJson)
    except Exception as e:
        return "Error: {}".format(str(e))
################################################################
########################## read html and print forms end #######
################################################################

################################################################
################## read html and send authentication ###########
################################################################
# fn to create forms form others servers
@app.route('/api/v1/settingConnAuth', methods=['GET','POST'])
def settingConnAuth():
    try:
        print("settingConnAuth >>")
        #setting = load_from_json_file("static/files/setting.json")
        url_download = "https://appgoyeneche1.herokuapp.com/static/files/setting.json?cache_id={}".format(uuid.uuid4())
        r = requests.get(url_download)
        setting = r.json()

        print("settingConnAuth >> setting >>")
        #print(setting)
        reserved = ["__message","__toUrl","url_file","__toEmail"]
        formdata = {}
        for item in setting:
            if item not in reserved:
                formdata.update({item: setting.get(item)})
        print(formdata)
        #print(setting.get("__toUrl"))
        #print(setting.get("__toEmail"))
        print("<< settingConnAuth << setting")

        formJson = {}
        ruwup = readUrlWithUtf8Pro(setting.get("__toUrl"))
        r = ruwup.get("r")
        s = ruwup.get("s")
        forms = readFormsFromStr(r.text)
        if len(forms) == 1:
            formJson = addChildNodeToForm(addHeaderToForm(addNewFormJson(), forms[0]), forms[0])
            formJson.update({"status":"OK"})
        elif len(forms)>2:
            formJson.update({"status":"This current version of App not support multi forms, contact your Developer"})
        else:
            formJson.update({"status":"Not detected form, review your URL"})

        print("<< settingConnAuth")

        currEl = formJson.get("currEl")
        for item in currEl:
            temp = formdata.get(item.get("name"))
            if temp is not None:
                item.update({"value":temp})
            if "value" not in item.keys():
                item.update({"value":""})
            item.pop("type", None)

        attr = formJson.get("attr")
        __toUrl = setting.get("__toUrl")
        action = attr.get("action")
        method = attr.get("method") if attr.get("method") is not None else "post"
        if action is not None:
            #if action.find("/") == 0:
                #p0 = __toUrl.rfind("/")
                #__toUrl = __toUrl[:p0]
            #action = "{}{}".format(__toUrl,action)
            action = "{}".format(__toUrl)
        else:
            action = "{}".format(__toUrl)
        attr.update({"action": action})
        attr.update({"method": method})

        #serial_cookies = ""
        #with open("static/files/cookie", 'rb') as f:
            #serial_cookies = pickle.dumps( s.cookies )
            #serial_cookies = f.read()
            #serial_cookies = pickle.loads( serial_cookies )
            #f.close()

        try:
            print("new version to auth >> ")
            data2 = {}
            for item in currEl:
                data2.update({item.get("name"):item.get("value")})
            print(json.dumps(data2))
            if attr.get("method") == "post":
                r = s.post(url = attr.get("action"), data=data2)
                formJson.update({"auth_status":str(r)})
                print("start download file... please wait...")
                r = s.get(url = setting.get("url_file"))
                formJson.update({"download_status":str(r)})
                output = open('static/files/current.xls', 'wb')
                output.write(r.content)
                output.close()
                print("it's finished downloading")
            else:
                formJson.update({"alert":"Witout support for this method {}".format(attr.get("method"))})
                print("Without support for this method {}".format(attr.get("method")))
            print("new version to auth << ")
        except Exception as e:
            print(e)
        return formJson
        #return render_template("api_connection.html", data=data, formJson=formJson)
    except Exception as e:
        return "Error: {}".format(str(e))
#from requests.auth import HTTPBasicAuth
#requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
#requests.get('https://api.github.com/user', auth=('user', 'pass'))
################################################################
################## read html and send authentication end #######
################################################################

def load_from_json_file(filename):
    """
    creates an Object from a "JSON file"
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_to_json_file(my_obj, filename):
    """
    writes an Object to a text file, using a JSON representation
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(my_obj, f)
