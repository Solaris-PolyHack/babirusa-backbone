import unique_codes as u_n
from flask import render_template, request, redirect, jsonify
from flask import Flask
from pymysql import connect as db_connect
import pymysql.cursors
import json
from flask_cors import CORS, cross_origin

return_res = False


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
CORS(app)


@app.route('/reg_tg', methods=['GET', 'POST'])
def reg_tg():
    if request.method == 'POST':
        user_dt = json.loads(request.data)
        with DBConnection() as db:
            result = db.read_once("SELECT * FROM users WHERE user_id_tg = %s", (user_dt['tg_id'],))
        if result is None:
            with DBConnection() as db:
                db.write_query(
                    "INSERT INTO users (user_id_tg, name, surname, user_class) VALUES (%s, %s, %s, %s)",
                    (user_dt['tg_id'], user_dt['name'], user_dt['surname'], user_dt['class']))
        else:
            return jsonify(result)


# @app.route('/change_tg', methods=['GET', 'POST'])
# def change_tg():
#     if request.method == 'POST':
#         user_dt = json.loads(request.data)
#         with DBConnection() as db:
#             result = db.read_once("SELECT * FROM users WHERE user_id_tg = %s", (user_dt['tg_id'],))
#         if result:
#             with DBConnection() as db:
#                 db.write_query("UPDATE users SET name = %s, surname = %s, class = %s WHERE id = %s",
#                                (user_dt['name'], user_dt['surname'], user_dt['class'], user_dt['tg_id']))
#             return 'change_accepted'
#         else:
#             return 'change_fall'


@app.route('/reg_tg_mail', methods=['GET', 'POST'])
def reg_tg_mail():
    if request.method == 'POST':
        user_dt = json.loads(request.data)
        with DBConnection() as db:
            result = db.read_once("SELECT * FROM users WHERE user_id_tg = %s", (user_dt['tg_id'],))
        if result is not None:
            with DBConnection() as db:
                db.write_query("UPDATE users SET password = %s, e_mail = %s WHERE id = %s",
                               (user_dt['password'], user_dt['e_mail'], user_dt['tg_id']))
            return 'added_successful'
        else:
            return 'add_fall'


@app.route('/log_tg_mail', methods=['GET', 'POST'])
def log_tg_mail():
    if request.method == 'POST':
        user_dt = json.loads(request.data)
        with DBConnection() as db:
            result = db.read_once("SELECT * FROM users WHERE user_id_tg = %s AND password = %s",
                                  (user_dt['e_mail'], user_dt['password']))
        if result is not None:
            with DBConnection() as db:
                db.write_query("UPDATE users SET user_id_tg = %s WHERE password = %s, e_mail = %s",
                               (user_dt['tg_id'], user_dt['password'], user_dt['e_mail']))
            return 'added_successful'
        else:
            return 'add_fall'


@app.route('/log_tg', methods=['GET', 'POST'])
def log_tg():
    if request.method == 'GET':
        with DBConnection() as db:
            result = db.read_once("SELECT * FROM users WHERE user_id_tg = %s", (request.args['tg_id'],))
    if result:
        result['status'] = 'ok'
        return jsonify(result)
    else:
        result = {}
        result['status'] = 'nouser'
        return jsonify(result)


@app.route('/reg_mb', methods=['GET', 'POST'])
def reg_mb():
    if request.method == 'POST':
        user_dt = json.loads(request.data)
        with DBConnection() as db:
            result = db.read_once("SELECT * FROM users WHERE e_mail = %s",
                                  (user_dt['e_mail'],))
        if result is None:
            token = u_n.token()
            with DBConnection() as db:
                db.write_query(
                    "INSERT INTO users (password, e_mail, name, surname, user_class) VALUES (%s, %s, %s, %s, %s)",
                    (user_dt['password'], user_dt['e_mail'], user_dt['name'], user_dt['surname'], user_dt['class']))
                db.write_query("INSERT INTO user_tokens (id, token) VALUES (%s, %s)", (user_dt['id'], token))
            return jsonify({'id': user_dt('id'), 'token': token})
        else:
            return 'created'


@app.route('/log_mb', methods=['GET', 'POST'])
def log_mb():
    if request.method == 'POST':
        token = u_n.token()
        user_dt = json.loads(request.data)
        with DBConnection() as db:
            result = db.read_once("SELECT * FROM users WHERE e_mail = %s AND password = %s",
                                  (user_dt['e_mail'], user_dt['password']))
        if result:
            with DBConnection() as db:
                db.write_query("INSERT INTO user_tokens (id, token) VALUES (%s, %s)", (result['id'], token))
            return jsonify({'user_date': jsonify(result), 'token': token})
        else:
            return 'log_fall'


@app.route('/session', methods=['GET', 'POST'])
def session():
    if request.method == 'POST':
        user_dt = json.loads(request.data)
        with DBConnection() as db:
            db.write_query(
                "INSERT INTO users (password, e_mail, name, surname, user_class) VALUES (%s, %s, %s, %s, %s)",
                (user_dt['password'], user_dt['e_mail'], user_dt['name'], user_dt['surname'], user_dt['class']))


@app.route('/code', methods=['GET', 'POST'])
def code():
    if request.method == 'GET':
        u_code = u_n.unique_code()
        with DBConnection() as db:
            db.write_query("INSERT INTO code_check (code, id) VALUES (%s, %s)", (u_code, 0))
        return u_code


@app.route('/code_check', methods=['GET', 'POST'])
def code_check():
    if request.method == 'POST':
        user_dt = json.loads(request.data)
        with DBConnection() as db:
            result = db.read_once("SELECT * FROM code_check WHERE code = %s",
                                  (user_dt['code'],))
        if result['id'] is not None:
            with DBConnection() as db:
                db.write_query("UPDATE code_check SET id = %s WHERE code = %s", (user_dt['tg_id'], user_dt['code']))
            return 'ok'
        else:
            return 'fall'
    if request.method == 'GET':
        with DBConnection() as db:
            result = db.read_once("SELECT * FROM code_check WHERE code = %s",
                                  (request.args['code'],))
        result['vscode_url'] = 'https://google.com'
        if result['id'] and result['vscode_url']:
            return jsonify({'status': 'ok', 'url': result['vscode_url']})
        elif result['id']:
            return jsonify({'status': 'creating'})
        else:
            return jsonify({'status': 'awaiting'})


app.run(host='10.66.66.33', port=2107, debug=True)
