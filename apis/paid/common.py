import abc
from os.path import join, dirname, realpath
import sqlite3
import logging

from ..common import MashapeAPI


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



class NoMoreFreeRequestsError(Exception):
	pass


class PaidAPI(MashapeAPI):

	def __init__(self):
		self.logger = logging.getLogger(self.name)
		self.api_db = APIDatabase()

	@abc.abstractproperty
	def free_requests(self):
		return 0

	def increment_requests(self):
		self.api_db.increment(self.name)

	@property
	def used_requests(self):
		return self.api_db.get_requests(self.name)

	@property
	def remaining_requests(self):
		requests = self.free_requests - self.used_requests
		self.logger.log(
			logging.WARNING if requests < 100 else logging.INFO, 
			"Remaining requests: {}/{}".format(requests, self.free_requests)
		)
		return requests

	def get(self, method, **kwargs):
		if self.remaining_requests < 1:
			raise NoMoreFreeRequestsError
		else:
			self.increment_requests()
			return MashapeAPI.get(self, method, **kwargs)
