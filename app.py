from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from functools import wraps
app = Flask(__name__)


app.secret_key = 'Login123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'amazon_login'

mysql = MySQL(app)
# def login_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print("Session:", session)
#         if 'loggedin' in session:
#             return func(*args, **kwargs)
#         else:
#             print("Redirecting to login")
#             return redirect(url_for('login'))
#     return wrapper

@app.route('/')
#@login_required
def home():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM amazon_accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['password'] = account['password']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM amazon_accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO amazon_accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
@app.route('/products')
def products():
    return render_template('products.html')


if __name__ == '__main__':
    app.run(debug=True)