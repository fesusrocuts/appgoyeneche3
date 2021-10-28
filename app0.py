import os.path
import uuid
import random
import firebase_admin
from firebase_admin import credentials
# Import the Firebase service
from firebase_admin import auth
from flask import Flask, request, render_template, \
    json, jsonify, redirect, url_for

cred = credentials.Certificate("secure/automatons-c6871-firebase-adminsdk-50b1p-810a407871.json")
# firebase_admin.initialize_app(cred)
config = '[DEFAULT]';
default_app = firebase_admin.initialize_app(cred, name=config)
print("--- default_app firebase ---")
print(default_app.name)
print("--- default_app firebase end ---")

##############################################
##############################################
print("--- add user ---")
try:
    # user = auth.get_user_by_phone_number(phone)
    # user = auth.get_user_by_email('dennisserocuts@gmail.com')
    # auth.delete_user(user.uid)
    # print('Successfully deleted user')

    user = auth.create_user(
        email='dennisserocuts@gmail.com',
        email_verified=True,
        phone_number='+573007330704',
        password='secretPassword',
        display_name='Dennisse Rocuts',
        photo_url='https://scontent.fbog4-1.fna.fbcdn.net/v/t1.0-1/c0.0.375.375a/69002801_2703142469906222_702382235575123968_n.jpg?_nc_cat=108&_nc_eui2=AeFhOyy9gQkIqR3g03x8Qn6dAQfurdZmjAciNRzgZ7PSWRGzDJqXHJOv4io2LUn-zRXnYINoa3q-2xm-OHqs_t_5weuay0T3SFu7ddIEhypEnA&_nc_ohc=ZMoXMPwdhBsAQm6spB3mC6SV8-NCy62nJKLH6rPQyHh6H0xP3ReycWB3Q&_nc_ht=scontent.fbog4-1.fna&oh=03c6cc68ba8baced10e573aebb51e921&oe=5E780E99',
        disabled=False)
    print('Sucessfully created new user: {0}'.format(user.uid))
except Exception as e:
    print("--- exception ---")
    print("<p>Error: %s</p>" % str(e) )
    print("--- exception end ---")
print("--- add user end ---")
##############################################
##############################################

##############################################
##############################################
"""
print("--- update user ---")
try:
    # auth.delete_user(uid)
    # print('Successfully deleted user')
    # user = auth.get_user_by_phone_number(phone)
    # user = auth.get_user_by_email(email)
    # user = auth.get_user_by_phone_number("+573227309677")
    user = auth.get_user_by_email("fesusrocuts@gmail.com")
    print("--- ---")
    print("get user by email")
    print(user)
    print("--- ---")
    user = auth.update_user(
        uid=user.uid,
        email='fesusrocuts@gmail.com',
        email_verified=True,
        phone_number='+573145702146',
        password='secretPassword',
        display_name='Fesus Rocuts',
        photo_url='https://avatars3.githubusercontent.com/u/2479899?s=460&v=4',
        disabled=False)
    print('Sucessfully update new user: {0}'.format(user.uid))
except Exception as e:
    print("--- exception ---")
    print("<p>Error: %s</p>" % str(e) )
    print("--- exception end ---")
print("--- update user end ---")
"""
##############################################
##############################################

##############################################
##############################################
# Start listing users from the beginning, 1000 at a time.
page = auth.list_users()
while page:
    for user in page.users:
        print('User: ' + user.uid)
    # Get next batch of users.
    page = page.get_next_page()

# Iterate through all users. This will still retrieve users in batches,
# buffering no more than 1000 users in memory at a time.
print("--- list_users ---")
for user in auth.list_users().iterate_all():
    print('User: ' + user.uid)
    #print(user.__dict__)
    print(user.__dict__["_data"].items())
print("--- list_users end ---")

##############################################
##############################################


# flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'
debug = True

@app.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test():
    data = request.get_json(force=True)
    print(data["key1"])
    print("----")
    print(data)
    print("----")
    response = {}
    response["message"] = 'Hi Fesus!'
    return jsonify(response)

@app.route('/create', methods=['GET', 'POST', 'PUT', 'DELETE'])
def create():
    data = request.get_json(force=True)
    print(data["key1"])
    print("----")
    print(data)
    print("----")
    response = {}
    response["message"] = 'Hi Fesus!'
    return jsonify(response)

@app.route('/')
def index():
    data = {
        "labels": {
            "title": "Service for building Automated Actions - Beta FR",
            "msg_welcome": "Welcome to the zone for building Automated Actions!",
            "author": "Fesus Rocuts, https://github.com/fesusrocuts, https://www.linkedin.com/in/fesus/",
            "btns": {
                "c": "create",
                "r": "read",
                "u": "update",
                "d": "delete"
            }
        },
        "cache_id": uuid.uuid4()
    }
    print("--- index ---")
    print(data)
    print("--- index ---")
    return render_template("index.html", data=data)


if __name__ == '__main__':
    app.run(debug=debug, threaded=True, host=host, port=port)
