"""
we are validating username and password with registered users
in database
"""

# --------------------
# Create App (Object) for our website
# --------------------
import flask
from flask_session import Session
from flask import session
provisioning_portal13 = flask.Flask(__name__)

provisioning_portal13.secret_key = "My secret password"
provisioning_portal13.config["SESSION_TYPE"] = "filesystem"
Session(provisioning_portal13)


# --------------------

# --------------------
# END POINT - 1 : http://127.0.0.1:5000/ URL MAPPED to '/'
# --------------------
@provisioning_portal13.route('/')
def my_index_page():
    return flask.render_template('index.html')

# --------------------

# --------------------
# END POINT - 2 : http://127.0.0.1:5000/about URL MAPPED to '/about'
# --------------------
@provisioning_portal13.route('/about')
def my_about_page():
    return flask.render_template('about.html')


# --------------------

# --------------------
# END POINT - 3 : http://127.0.0.1:5000/login URL MAPPED to '/login'
# --------------------
@provisioning_portal13.route('/login')
def my_login_page():
    return flask.render_template('login.html')


# --------------------

# --------------------
# END POINT - 4 : http://127.0.0.1:5000/validate URL MAPPED to '/validate'
# --------------------
@provisioning_portal13.route('/validate', methods=['POST'])
def my_validate_page():
    # Task - 1 : Get user name & pass word entered by user
    # ----------------
    # framework will keep all the form data entered by use in a dictionary.
    # dictionary is 'flask.request.form'. from this dictionary we can retrieve username & password
    # key will be 'uname' and 'pw'
    entered_username = flask.request.form.get('uname')
    entered_password = flask.request.form.get('pw')
    entered_username = entered_username.lower()
    entered_username = entered_username.strip()
    # Connect to user_db.sqlite, check whether entered username and password
    # present. If not present then return login failed
    import sqlite3

    print("Create/Connect to database 'users_db.sqlite' ")
    my_db_connection = sqlite3.connect(r'users_db.sqlite')
    print("Done")

    print("Get cursor object, which help us to execute SQL query on database ")
    my_db_cursor = my_db_connection.cursor()
    print("Done")
    print("Check whether table exist")
    my_db_cursor.execute(f" SELECT name FROM sqlite_master WHERE type='table' AND name='users_table'; ")
    print("Done")

    print("Retrieve all data from cursor")
    my_db_result = my_db_cursor.fetchall()
    print("Done")

    if len(my_db_result) == 0:
        return "<center>First Register to login<br><a href='/newuser'>Back</a></center>"

    print("Executing select query")
    my_db_cursor.execute(
        f"SELECT NAME, PASSWORD FROM USERS_TABLE WHERE NAME='{entered_username}' AND PASSWORD = '{entered_password}'")
    print("Done")

    print("Retrieve all data from cursor")
    my_db_result = my_db_cursor.fetchall()
    print("Done")
    # if we get record then username & password correct else wrong

    # This work is done, so close db connection
    my_db_connection.close()

    if len(my_db_result) > 0:

        #store username in session object
        session['username'] = entered_username

        # All the data is in my_db_result
        return "Login Success"

    else:
        return "Login Failed. Invalid Credentials <br><br> <a href='/login'>Go Back To Login</a>"


# ----------------
# POINTS - 1
# ----------------
# - We are sending data inside python object to html file
# - If we need to display python variable in html then we need to
#   write python code inside html
# - We can write python code inside html file using below syntax
#   1) Use this {{variable_name}} to display any python variable value
#   2) Use this {% to write any python code %}
#   3) Use this {% if condn%}  for any block like if, for etc
#               {% endif %}
# ----------------
# --------------------

# --------------------
# END POINT - 5 : http://127.0.0.1:5000/newuser URL MAPPED to '/newuser'
# --------------------
@provisioning_portal13.route('/newuser')
def my_newuser_page():
    return flask.render_template('newuser.html')
# --------------------

# END POINT - 6 : http://127.0.0.1:5000/register URL MAPPED to '/register'
# --------------------
@provisioning_portal13.route('/register', methods=['POST'])
def my_register_page():
    # Get all data
    entered_username = flask.request.form.get('uname')
    entered_password_1 = flask.request.form.get('pw1')
    entered_password_2 = flask.request.form.get('pw2')
    entered_email = flask.request.form.get('email')
    entered_username = entered_username.lower()
    entered_username = entered_username.strip()
    # Check whether both the passwords are matching
    if entered_password_1 != entered_password_2:
        return "Both Passwords Are Not Matching. <br><br><a href='/login'>Go Back To Registration</a>"

    # Create Database and table if not present
    import sqlite3

    print("Create/Connect to database 'users_db.sqlite' ")
    my_db_connection = sqlite3.connect('users_db.sqlite')
    print("Done")

    print("Get cursor object, which help us to execute SQL query on database ")
    my_db_cursor = my_db_connection.cursor()
    print("Done")

    print("Create table if not exists")
    my_query = '''CREATE TABLE IF NOT EXISTS users_table(
    NAME    VARCHAR(100),
    PASSWORD    VARCHAR(100),
    EMAIL   VARCHAR(100)
    )
    '''
    my_db_cursor.execute(my_query)
    print("Done")
    # ------------------------

    # verify whether user already exists in the database
    # How? select from table where username = entered_username
    # if we get records then we decide found
    # if we get 0 records the we can decide not found
    my_query = f"SELECT * FROM users_table WHERE name='{entered_username}'"
    my_db_cursor.execute(my_query)
    my_db_result = my_db_cursor.fetchall()
    if len(my_db_result) > 0:
        return "User Already Exists. <br><br><a href='/login'>Go Back To Registration</a>"

    # if user not exists then add new record to database and return account created successfully
    my_query = f"INSERT INTO USERS_TABLE VALUES('{entered_username}', '{entered_password_1}', '{entered_email}')"
    my_db_cursor.execute(my_query)
    my_db_connection.commit()
    my_db_connection.close()
    return "User Created Successfully. <a href='/login'>Click Here To Login</a>"


#---------------------
# END POINT - 7 : http://127.0.0.1:5000/newclient URL MAPPED to '/newclient'
# --------------------
@provisioning_portal13.route('/newclient')
def my_addnewclient_page():
    return flask.render_template('newclient.html')
# --------------------
# --------------------
# END POINT - 8 : http://127.0.0.1:5000/newclient URL MAPPED to '/newclient'
# --------------------
@provisioning_portal13.route('/newclient', methods=['POST'])
def my_newclient_page():
    # Get all data
    entered_customername = flask.request.form.get('cname')
    entered_location = flask.request.form.get('loc')
    entered_email = flask.request.form.get('email')
    entered_phone = flask.request.form.get('phone')
    entered_cpu = flask.request.form.get('cpu')
    entered_storage = flask.request.form.get('storage')
    entered_memory = flask.request.form.get('memory')
    entered_assignedto = flask.request.form.get('assignto')
    entered_customername = entered_customername.lower()
    entered_customername = entered_customername.strip()

    # Create Database and table if not present
    import sqlite3

    print("Create/Connect to database 'users_db.sqlite'")
    my_db_connection = sqlite3.connect('users_db.sqlite')
    print("Done")

    print("Get cursor object, which help us to execute SQL query on database")
    my_db_cursor = my_db_connection.cursor()
    print("Done")

    print("Create table")
    my_query = '''CREATE TABLE IF NOT EXISTS new_client_table(
    CUSTOMERNAME   VARCHAR(100),
    SERVICEREQUESTID INTEGER PRIMARY KEY AUTOINCREMENT,
    LOCATION    VARCHAR(100),
    EMAIL    VARCHAR(100),
    PHONE    INTEGER,
    CPU    VARCHAR(100),
    STORAGE    INTEGER,
    MEMORY    INTEGER,    
    ASSIGNEDTO   VARCHAR(100)
    
    )
    '''
    my_db_cursor.execute(my_query)
    print("Done")
    # ------------------------

    # if user not exists then add new record to database and return account created successfully
    my_query = f"INSERT INTO NEW_CLIENT_TABLE(CUSTOMERNAME,LOCATION,EMAIL,PHONE,CPU,STORAGE,MEMORY,ASSIGNEDTO)VALUES('{entered_customername}','{entered_location}','{entered_email}','{entered_phone}','{entered_cpu}','{entered_storage}','{entered_memory}','{entered_assignedto}')"
    my_db_cursor.execute(my_query)
    my_db_connection.commit()
    my_db_connection.close()
    return "Added client application. <a href='/#'>Click Here to continue</a>"

# --------------------
# END POINT - 9 : http://127.0.0.1:5000/newclient URL MAPPED to '/newclient'
# --------------------
@provisioning_portal13.route('/clientdetailspage')
def my_viewclient_page():
    return flask.render_template('clientdetails.html')


# --------------------
# END POINT - 10 : http://127.0.0.1:5000/clientdetails URL MAPPED to '/clientdetails'
# --------------------
@provisioning_portal13.route('/clientdetails', methods=['GET'])
def my_clientdetails_page():

    # Create Database and table if not present
    import sqlite3

    print("Create/Connect to database 'users_db.sqlite'")
    my_db_connection = sqlite3.connect(r'users_db.sqlite')
    print("Done")

    print("Get cursor object, which help us to execute SQL query on database")
    my_db_cursor = my_db_connection.cursor()
    print("Done")

    print("Executing select query")
    my_db_cursor.execute('SELECT * FROM NEW_CLIENT_TABLE')
    print("Done")

    print("Retrieve all data from cursor")
    my_db_result = my_db_cursor.fetchall()
    print("Done")
    print("result=",my_db_result)
    # All the data is in my_db_result
    return flask.render_template('clientdetails.html', my_data=my_db_result)


# --------------------
# END POINT - 11 : http://127.0.0.1:5000/logout URL MAPPED to '/logout'
# --------------------
@provisioning_portal13.route('/logout')
def my_logout_page():
    session['username'] = None
    return flask.render_template('logout.html')

# --------------------
# Run the server
# --------------------
provisioning_portal13.run()
# --------------------
