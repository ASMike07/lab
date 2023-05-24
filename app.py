import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(user="postgres",
                        database="service_db",
                        password="deadmike07",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/', methods=['POST'])
def login():
    username = request.form.get('login')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(login), str(password)))
    records = list(cursor.fetchall())

    if records == []:
        return render_template("account.html")

    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
