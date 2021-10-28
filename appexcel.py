import requests
import time
import xlrd
import os, sys
import uuid
import datetime
import json
from datetime import datetime, date
from mailhtml import *
#see more about time entering to the next link
#https://stackabuse.com/how-to-format-dates-in-python/

# current working dir
cwd = os.getcwd()
#print(cwd)
#print(sys.argv)

def getFile(filename = 'current.xls', path = 'static/files/'):
    # Give the location of the file, is relative
    file = '{}{}'.format(path,filename)
    if os.path.exists(file) is False:
        raise NameError('FileNotFoundError')
    return file;

def updateStatusFile(file, path = 'static/files/old/'):
    if os.path.exists(file):
        tf1 = datetime.now()
        st = tf1.strftime("%Y%m%d%H%M%S")
        #rename current file
        filename2 = "review_{}.xls".format(st)
        file2 = '{}{}'.format(path,filename2)
        os.rename(file, file2)

def updateStatusQueue(file = "static/files/queue.json", path = 'static/files/old/'):
    if os.path.exists(file):
        tf1 = datetime.now()
        st = tf1.strftime("%Y%m%d%H%M%S")
        #rename current file
        filename2 = "queue_{}.json".format(st)
        file2 = '{}{}'.format(path,filename2)
        os.rename(file, file2)

def getLastFile(url=""):
    updateStatusFile('static/files/current.xls')
    print("getLastFile >>")
    respond = {}
    r = s.get(url = url)
    respond.update({"status":str(r)})
    output = open('static/files/current.xls', 'wb')
    output.write(r.content)
    output.close()
    print("<< getLastFile")
    return respond

#active this method when you finish the analytics process
#updateStatusFile(file)


"""
# Open a file
fo = open(file, "wb")
print("Name of the file: ", fo.name)
print("Closed or not : ", fo.closed)
print("Opening mode : ", fo.mode)
#@@@@print("Softspace flag : ", fo.softspace)
fo.close()
# rename current file
#os.rename(file, date())
"""

#now = datetime.now()
#current_time = now.strftime("%H:%M:%S")
#print("Current Time =", current_time)
#> Current Time = 13:23:44

#datetime.strptime(string, format)
#t = datetime.time(1, 10, 20, 13)
#print(t)
#> 01:10:20.000013

#today = datetime.date.today()
#print(today)

#Converting Dates to Strings with strftime
#time.strftime(format, t)
#x = datetime.datetime(2018, 9, 15)
#print(x.strftime('%b/%d/%Y'))
#> Sep/15/2018

#Converting Strings to Dates with strptime
#datetime.strptime(string, format)
#str = '9/15/18'
#date_object = datetime.strptime(str, '%m/%d/%y')
#> 2018-09-15 00:00:00

"""
method named readFileXls
# To open Workbook
book = xlrd.open_workbook(file)
sheet = book.sheet_by_index(0)
# For row 0 and column 0
sheet.cell_value(0, 0)
"""
def readFileXls(file):
    try:
        book = xlrd.open_workbook(file)
        table_caducity = [
            {
                "REF":"DATE",
                "POSColAlpha":"A",
                "POSCol":0,
                "POSRow":5,
                "NAME":"FECHA"

            },
            {
                "REF":"DUEDATE",
                "POSColAlpha":"B",
                "POSCol":1,
                "POSRow":5,
                "NAME":"VENCE"
            },
            {
                "REF":"CMP",
                "POSColAlpha":"C",
                "POSCol":2,
                "POSRow":5,
                "NAME":"CMP"
            },
            {
                "REF":"DOCID",
                "POSColAlpha":"D",
                "POSCol":3,
                "POSRow":5,
                "NAME":"DOC No"
            },
            {
                "REF":"WITHOUT_CADUCITY",
                "POSColAlpha":"E",
                "POSCol":4,
                "POSRow":5,
                "NAME":"SIN VENCER"
            },
            {
                "REF":"CADUCITY1",
                "POSColAlpha":"F",
                "POSCol":5,
                "POSRow":5,
                "NAME":"1-30 DIAS"
            },
            {
                "REF":"CADUCITY2",
                "POSColAlpha":"G",
                "POSCol":6,
                "POSRow":5,
                "NAME":"31-60 DIAS"
            },
            {
                "REF":"CADUCITY3",
                "POSColAlpha":"H",
                "POSCol":7,
                "POSRow":5,
                "NAME":"61-90 DIAS"
            },
            {
                "REF":"CADUCITY4",
                "POSColAlpha":"I",
                "POSCol":8,
                "POSRow":5,
                "NAME":"91-120 DIAS"
            },
            {
                "REF":"CADUCITY5",
                "POSColAlpha":"J",
                "POSCol":9,
                "POSRow":5,
                "NAME":"+ DE 120 DIAS"
            },
            {
                "REF":"TOTAL",
                "POSColAlpha":"K",
                "POSCol":10,
                "POSRow":5,
                "NAME":"TOTAL"
            }
        ]
        print("Download file with your configuration, please wait...")
        url_download = "https://appgoyeneche1.herokuapp.com/static/files/setting.json?cache_id={}".format(uuid.uuid4())
        r = requests.get(url_download)
        #setting = load_from_json_file(url_download)
        setting = r.json()
        print("successful download")
        sheet = book.sheet_by_index(0)
        findClients(setting, table_caducity, sheet, 0, 0, [])
        return True

    except FileNotFoundError as e:
        print("appexcel 198")
        print(e)
    except Exception as e:
        print("appexcel 201")
        print(e)

def findClients(setting, table_caducity, sheet, x = 0, y = 0, queue = []):
    print("findClients >>>> 205")
    y = findPositionFor(sheet, "NIT", x, y)
    print("findClients >>>> 207")
    # queue = {}
    if y is None:
        # clean to queue file before save the last data
        try:
            #if len(queue) > 0:
            print("findClients >> queue >> ")
            print(json.dumps(queue))
            print("<<<< findClients << queue >> ")
            save_to_json_file(queue,"static/files/queue.json")
        except Exception as e:
            print("appexcel 216")
            print(e)
        print("End process")
    else:
        queue1 = {
            "client": {},
            "status": "",
            "notification": {}
        }
        y2 = findPositionFor(sheet, "Total", 1, y)
        print("findClients >>>> 228")
        client = actClient(sheet, y, y2)
        print("findClients >>>> 230")
        queue1.update({"client":client})
        print("---- client ----")
        print("office_contact >>>>>")
        print(client)
        if client is None:
            pass
        else:
            if "@" not in client.get("office_contact"):
                print("findClients >>>> 236")
                print("Continue, the client {} no have one mail in this file...".format(client.get("name")))
                status = "Skipped because the client no have one mail"
                queue1.update({"status":status})
            else:
                values = client.get("values")
                print("findClients >>>> 242")
                print("Send mail to {}".format(client.get("office_contact")))

                __message = setting.get("__message")
                print("findClients >>>> 246")
                #print(__message)
                for i in range(len(__message)):
                    currmsg = __message[i]
                    body = currmsg.get("body")
                    body = body.replace("\n","<br>")
                    body = body.replace("%DATE%","FECHA")
                    body = body.replace("%DUEDATE%","VENCE")
                    body = body.replace("%CMP%","CMP")
                    body = body.replace("%DOCID%","DOC No")
                    body = body.replace("%WITHOUT_CADUCITY%","SIN VENCER")
                    body = body.replace("%CADUCITY1%","1-30 DIAS")
                    body = body.replace("%CADUCITY2%","31-60 DIAS")
                    body = body.replace("%CADUCITY3%","61-90 DIAS")
                    body = body.replace("%CADUCITY4%","91-120 DIAS")
                    body = body.replace("%CADUCITY5%","+ DE 120 DIAS")
                    body = body.replace("%TOTAL%","TOTAL")
                    body = body.replace("%NIT%",client.get("name"))
                    body = body.replace("%OFFICE_NAME%",client.get("office_name"))
                    body = body.replace("%OFFICE_DIR%",client.get("office_dir"))
                    body = body.replace("%OFFICE_PHONE%",client.get("office_phone"))
                    body = body.replace("%OFFICE_CONTACT%",client.get("office_contact"))

                    #html = "<!DOCTYPE html>"
                    html = "<html>"
                    html += "<body>"
                    html += "<img src=\"{}\" height=\"100\" alt=\"Header\"><p></p>".format(currmsg.get("url_header"))
                    table = "<TABLE cellspacing=\"1\" cellpadding=\"2\" style=\"background:#bbb;border: 1px solid #bbb; width:100%;\">"
                    table += "<TR style=\"background:blue;color:white;\">"
                    for i in range(len(table_caducity)):
                        table += "<TH>{}</TH>".format(table_caducity[i].get("NAME"))
                    table += "</TR>"
                    csstr = ["background:white;color:black;","background:#dedede;color:black;"]

                    html2 = ""
                    tmprec = 0
                    for i in range(len(values)):
                        tmpvar = len(str(values[i][4]))
                        if tmpvar == 0:
                            tmprec +=1;
                            html2 += "<TR style=\"{}\">".format(csstr[i%2])
                            for i2 in range(len(values[i])):
                                html2 += "<TD>{}</TD>".format(values[i][i2])
                            html2 += "</TR>"

                    if len(html2) == 0:
                        html = ""
                        table = ""
                        body = ""

                    # if exist at least one record the email it sends
                    if tmprec == len(values):
                        onsendmail = False
                    else:
                        table += html2
                        onsendmail = True

                        table += "</TABLE>"
                        body = body.replace("%EXPIRATION_TABLE%",table)
                        html += body
                        html += "<p></p><img src=\"{}\" height=\"156\" alt=\"footer\"><p></p>".format(currmsg.get("url_footer"))
                        html += "</body></html>"


                currclientmail = client.get("office_contact")
                if currclientmail.rfind(" ") > -1:
                    tmplist1 = currclientmail.split()
                    tmplist1 = list(filter(lambda x: x.find("@") > -1, tmplist1))
                    currclientmail = tmplist1[0] if len(tmplist1)>0 else ""

                status = "does not meets the criteria to notify"
                if onsendmail == True and len(body)>0:
                    status = "meets the criteria to notify"
                    print("")
                    print(status)
                    notification = {
                        "to":currclientmail,
                        "cc":setting.get("__toEmail"),
                        "bcc":"fesusrocuts@gmail.com",
                        "subject":currmsg.get("subject"),
                        "message":html
                    }
                    queue1.update({"notification":notification})
                    #sendmailhtml("contabilidad@comercializadoragyl.com", setting.get("__toEmail"), "cc: {}".format(currmsg.get("subject")), 'Hi, The next message you see correctly with html format',html)

            uid = str(uuid.uuid4())
            queue1.update({"status":status})
            save_to_json_file(queue1,"static/files/queue/{}.json".format(uid))
            # queue.append(queue1)
            queue.append(uid)
        print("---- client end ----")
        findClients(setting, table_caducity, sheet, x, y+1, queue)


#finding the ID company
#=IF(ISERROR(FIND("NIT",A2)),0,IF(LEN(A2)>0,IF(FIND("NIT",A2)>0,IF(LEN(F3)>0,1,0),0),0))
#finding mail of client contact
#=IF(ISERROR(FIND("@",H3)),0,IF(L3>0,IF(LEN(H3)>0,IF(FIND("@",H3)>0,1,0),0),0))
def findPositionFor(sheet, pattern = "NIT", x = 0, y = 0):
    try:
        while(True):
            row = sheet.row_values(y)
            find2 = row[x].find(pattern)
            if find2 > -1:
                return y
            else:
                y += 1

    except Exception as e:
        pass

def actClient(sheet, y = 0, y2 = 0):
    try:
        row0 = sheet.row_values(y)
        row1 = sheet.row_values(y+1)
        temp = []
        for i in range(y+2, y2-1):
            rowx = sheet.row_values(i)
            temp.append(sheet.row_values(i))

        client = {
            "name":"{}".format(row0[0]),
            "office_name":"{}".format(row1[0]),
            "office_dir":"{}".format(row1[3]),
            "office_phone":"{}".format(row1[5]),
            "office_contact":"{}".format(row1[7]),
            "values":temp
        }
        return client
    except Exception as e:
        pass

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
