import requests
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="deadmike07",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username:
        return render_template('login.html', error='Введите логин')
    if not password:
        return render_template('login.html', error='Введите пароль')
    cursor.execute("SELECT * FROM service.users WHERE username=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if records == []:
        return render_template('account.html')
    return render_template('account.html', full_name=records[0][1], username=records[0][2], password=records[0][3])

if __name__ == '__main__':
    app.run(debug=True)

