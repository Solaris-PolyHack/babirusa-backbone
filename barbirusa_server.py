from flask import render_template, request, redirect
from flask import Flask
from pymysql import connect as db_connect
import pymysql.cursors
import json


class DBConnection():
    hostname = "10.66.66.27"
    username = "babirusa"
    password = "babirusa"
    db = 'babirusa'

    def __enter__(self):
        self.connection = db_connect(host=self.hostname,
                                     user=self.username,
                                     password=self.password,
                                     database=self.db,
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        return self

    def read_once(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def read_all(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def write_query(self, query, params):
        self.cursor.execute(query, params)
        self.connection.commit()

    def __exit__(self, type, value, traceback):
        self.connection.close()


app = Flask(__name__)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        user_dt = json.loads(request.data)
        with DBConnection() as db:
            results = db.read_all("SELECT * FROM users WHERE user_id = %s AND user_id_tg = %s",
                                  (user_dt['tg_id'], user_dt['tg_id']))
        if results == ():
            with DBConnection() as db:
                db.write_query(
                    "INSERT INTO users (user_id_tg, name, surname, user_class) VALUES (%s, %s, %s, %s)",
                    (user_dt['tg_id'], user_dt['name'], user_dt['surname'], user_dt['class']))
    return 'ok'


app.run(host='10.66.66.33', port=2107)