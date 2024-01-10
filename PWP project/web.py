from flask import Flask, render_template, session, request, redirect, url_for
import re  
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '!@#$%'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'web'
mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def login():
    login_alert = ''  
    if request.method == 'POST' and 'inpUser' in request.form and 'inpPass' in request.form:
        username = request.form['inpUser']
        password = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users where username = %s and password = %s", (username, password))
        data = cur.fetchone()
        cur.close()
        if data:
            session['is_logged_in'] = True
            session['email'] = data[1]
            return redirect(url_for('home'))
        else:
            login_alert = 'username atau password salah! Silahkan coba lagi!'
    return render_template('login.html', login_alert=login_alert)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    msg2 = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not username or not password or not email:
            msg = 'Please fill out the form!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM users WHERE username = %s', (username, ))
            account = cur.fetchone()
            if account:
                msg = 'Account already exists!'
            else:
                cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
                mysql.connection.commit()
                msg2 = 'Daftar berhasil. Silahkan kembali ke halaman login!'
    return render_template('register.html', msg=msg, msg2=msg2) 

@app.route('/home')
def home():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.close()
        return render_template('home.html', users=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/kelas')
def kelas():
    return render_template('kelas.html')


@app.route('/langganan', methods=['GET', 'POST'])
def langganan():
    msg = ''
    msg2 = ''
    if request.method == 'POST':
        name = request.form['nama']
        course = request.form['course']
        alamat = request.form['alamat']
        harga = request.form['harga']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO beli_paket (nama, course, alamat, harga) VALUES (%s, %s, %s, %s)', (name, course, alamat, harga))
        mysql.connection.commit()
        msg2 = 'Pembelian Berhasil!'
        return redirect(url_for('detail'))
    return render_template('langganan.html', msg=msg, msg2=msg2)

@app.route('/detail', methods=['GET', 'POST'])
def detail():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM beli_paket")
        detail=cur.fetchall()
        return render_template('detail.html', detail=detail)
    else:
        return redirect(url_for('langganan'))

@app.route('/kontak')
def kontak():
    return render_template("kontak.html")

@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
