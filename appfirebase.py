import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Import the Firebase service
from firebase_admin import auth
from appbase import app

################################################################
########################## firebase ############################
################################################################
url = ""
cred = credentials.Certificate("secure/automatons-c6871-firebase-adminsdk-50b1p-810a407871.json")
# firebase_admin.initialize_app(cred)
config = '[DEFAULT]';
default_app = firebase_admin.initialize_app(cred, name=config)
print("--- default_app firebase ---")
print(default_app.name)
print("--- default_app firebase end ---")

print("--- default_app firebase db ---")
db = firestore.client()
print(db)
print("--- default_app firebase db end ---")
################################################################
########################## firebase end ########################
################################################################


################################################################
########################## firebase info #######################
################################################################
@app.route('/get_storage_link', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_storage_link():
    print("see data in https://console.cloud.google.com/firestore/data?project=automatons-c6871")
    return("https://console.cloud.google.com/firestore/data?project=automatons-c6871")
################################################################
########################## firebase info end ###################
################################################################


################################################################
########################## firebase test #######################
################################################################
@app.route('/db/collection/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
def db_collection_test():
    print("--- default_app firebase db users_ref ---")
    test_ref = db.collection(u'test')
    print(test_ref)
    print(test_ref.__dict__)
    docs = test.stream()
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    print("--- default_app firebase db test_ref end ---")
    return test_ref
################################################################
########################## firebase test end ###################
################################################################



################################################################
########################## firebase auth user ##################
################################################################
@app.route('/delete_user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def delete_user():
    try:
        # user = auth.get_user_by_phone_number(phone)
        user = auth.get_user_by_email('dennisserocuts@gmail.com')
        auth.delete_user(user.uid)
        print('Successfully deleted user')
        return 'Successfully deleted user'
    except Exception as e:
        print("--- exception ---")
        print("<p>Error: %s</p>" % str(e) )
        print("--- exception end ---")
        return "<p>Error: %s</p>" % str(e)


@app.route('/create_user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def create_user():
    try:
        # user = auth.get_user_by_phone_number(phone)
        # user = auth.get_user_by_email('dennisserocuts@gmail.com')
        # auth.delete_user(user.uid)
        # print('Successfully deleted user')
        user = auth.create_user(
            email='dennisserocuts@gmail.com',
            email_verified=False,
            phone_number='+573007330703',
            password='secretPassword',
            display_name='Dennisse Rocuts',
            photo_url='https://scontent.fbog4-1.fna.fbcdn.net/v/t1.0-1/c0.0.375.375a/69002801_2703142469906222_702382235575123968_n.jpg?_nc_cat=108&_nc_eui2=AeFhOyy9gQkIqR3g03x8Qn6dAQfurdZmjAciNRzgZ7PSWRGzDJqXHJOv4io2LUn-zRXnYINoa3q-2xm-OHqs_t_5weuay0T3SFu7ddIEhypEnA&_nc_ohc=ZMoXMPwdhBsAQm6spB3mC6SV8-NCy62nJKLH6rPQyHh6H0xP3ReycWB3Q&_nc_ht=scontent.fbog4-1.fna&oh=03c6cc68ba8baced10e573aebb51e921&oe=5E780E99',
            disabled=False)
        print('Sucessfully created new user: {0}'.format(user.uid))
        return user.__dict__["_data"]
    except Exception as e:
        print("--- exception ---")
        print("<p>Error: %s</p>" % str(e) )
        print("--- exception end ---")
        return "<p>Error: %s</p>" % str(e)


@app.route('/update_user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def update_user():
    try:
        # auth.delete_user(uid)
        # print('Successfully deleted user')
        # user = auth.get_user_by_phone_number(phone)
        # user = auth.get_user_by_email(email)
        # user = auth.get_user_by_phone_number("+573227309677")
        user = auth.get_user_by_email('dennisserocuts@gmail.com')
        user = auth.update_user(
            uid=user.uid,
            email_verified=False,
            phone_number='+573007330704',
            disabled=False)
        print('Sucessfully update new user: {0}'.format(user.uid))
        return user.__dict__["_data"]
    except Exception as e:
        print("--- exception ---")
        print("<p>Error: %s</p>" % str(e) )
        print("--- exception end ---")
        return "<p>Error: %s</p>" % str(e)


@app.route('/list_users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def list_users():
    try:
        # Start listing users from the beginning, 1000 at a time.
        # page = auth.list_users()
        # while page:
            # for user in page.users:
                # print('User: ' + user.uid)
            # Get next batch of users.
            # page = page.get_next_page()

        # Iterate through all users. This will still retrieve users in batches,
        # buffering no more than 1000 users in memory at a time.
        users = {}
        for user in auth.list_users().iterate_all():
            print('User: ' + user.uid)
            #print(user.__dict__)
            print(user.__dict__["_data"].items())
            users[user.uid] = user.__dict__["_data"]
        return users
    except Exception as e:
        print("--- exception ---")
        print("<p>Error: %s</p>" % str(e) )
        print("--- exception end ---")
        return "<p>Error: %s</p>" % str(e)


@app.route('/auth2', methods=['GET', 'POST', 'PUT', 'DELETE'])
def auth2():
    try:
        # data = request.get_json(force=True)
        user = auth.get_user_by_email('dennisserocuts@gmail.com')
        response = {
            "status":"success",
            "token":user.uid
        }
        print("----- auth -----")
        print(user.uid)
        print("----- auth end -----")
        #subcredential = firebase.auth.EmailAuthProvider.credential('dennisserocuts@gmail.com', 'secretPassword');
        #print(subcredential)
        return response
    except Exception as e:
        response = {
            "status":"fail",
            "token":""
        }
        return response
################################################################
########################## firebase auth user end ##############
################################################################
