from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

app = Flask(__name__)

#Configure Db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Registration'

mysql = MySQL(app)

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        #Fetching data
        details = request.form
        name = details['name']
        email = details['email']
        password = details['password'].encode('utf-8')

        #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO users (name,email,password) VALUES (%s, %s, %s)",(name, email, password))

        # getting error :- work upon it ---
        #cur.execute(f"INSERT INTO users (name,email,password) VALUES (%s, %s, %s)", (name, email, hash_password))
        mysql.connection.commit()
        session['name'] = name
        session['email'] = email
        cur.close()
        return redirect(url_for('index'))
    else:
        return render_template('registration.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            #Invalid salt error:- -- work on it
            # if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
            if user['password'].encode('utf-8') == password:
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template('index.html')
            else:
                return "Incorrect password"
        else:
            return "Error password or user not match"
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = "012#!APaAjaBoleh)(*^%"
    app.run(debug=True)
