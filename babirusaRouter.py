from mitmproxy import http
from pymysql import connect as db_connect
import pymysql.cursors

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

def request(flow: http.HTTPFlow) -> None:
    flow.request.headers["Host"] = "codeat.babirusa.skifry.ru"