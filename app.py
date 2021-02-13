from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__, static_url_path="")
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'

mysql = MySQL(app)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/dbuku")
def dbuku():
    return render_template('dbuku.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email, password) VALUES(%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('signin'))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return redirect(url_for('dashboard.html'))
        else:
                return "Error password and email salah"
    return render_template('signin.html')

@app.route("/dashboard")
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM buku")
    rv = cur.fetchall()
    cur.close()
    return render_template('dashboard.html',bukus=rv)

@app.route("/tambah", methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        buku = request.form['buku']
        jumlah = request.form['jumlah']
        val = (buku,jumlah)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO buku (buku, jumlah) VALUES (%s, %s)",val)
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('tambah.html')

@app.route("/edit/<id_buku>", methods=["POST"])
def edit(id_buku):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM buku WHERE id_buku=%s", (id_buku,))
    data = cur.fetchone()
    if request.method == 'POST':
        id_buku = request.form['id_buku']
        buku = request.form['buku']
        jumlah = request.form['jumlah']
        val = (id_buku,buku,jumlah)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE buku SET buku=%s, jumlah=%s WHERE id_buku=%s", val)
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template('edit.html',data=data)

@app.route('/delete/<id_buku>', methods=['GET', 'POST'])
def delete(id_buku):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM buku WHERE id_buku=%s', (id_buku,))
    mysql.connection.commit()
    return redirect(url_for('dashboard'))

@app.route("/member")
def member():
    return render_template('member.html')

@app.route("/forms")
def form():
    return render_template('forms.html')

@app.route("/tables")
def tables():
    return render_template('tables.html')

if __name__ == "__main__":
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug = True)