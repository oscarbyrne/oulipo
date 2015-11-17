import requests
from os.path import join, dirname, realpath
import sqlite3

from ..keys import mashape_key


headers = {
    "X-Mashape-Key": mashape_key,
    "Accept": "application/json",
}

def get(api_name, method, **kwargs):
    url = "https://{}.p.mashape.com/{}".format(api_name, method)
    return requests.get(url, headers=headers, **kwargs).json()


class APIDatabase(object):

    name = join(dirname(realpath(__file__)), "requests.db")

    def __init__(self):
        self.create_table()

    def execute(self, string, *args):
        with sqlite3.connect(self.name) as con:
            con.execute(string, args)
            con.commit()

    def query(self, string, *args):
        with sqlite3.connect(self.name) as con:
            cur = con.cursor()
            cur.execute(string, args)
            return cur.fetchall()

    def create_table(self):
        self.execute("CREATE TABLE IF NOT EXISTS Requests (name TEXT PRIMARY KEY, requests INT)")

    def drop_table(self):
        self.execute("DROP TABLE IF EXISTS Requests")

    def reset_table(self):
        self.drop_table()
        self.create_table()

    def get_table(self):
        return self.query("SELECT * FROM Requests")

    def insert(self, name, requests):
        self.execute("INSERT OR REPLACE INTO Requests VALUES(?,?)", name, requests)

    def get_requests(self, name):
        ret = self.query("SELECT requests FROM Requests WHERE name=?", name)
        if len(ret) == 0:
            return 0
        else:
            return ret[0][0]

    def increment(self, name):
        n = self.get_requests(name)
        self.insert(name, n+1)
