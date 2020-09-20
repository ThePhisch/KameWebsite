import pymysql

class Connector():
	"""
	Class to connect to MariaDB
	Provides helper functions and especially an abstraction layer so database does not
	have to be opened to remote access.
	Usecases:
	* Getting/Saving Progress
	* Validating login of User
	"""
	def __init__(self, db='ulrich_offline', user='anton', passwd='anton',host='localhost'):
		"""
		Initialise Connection to database
		"""
		self.db = db
		self.user = user
		self.passwd = passwd
		self.host = host
		self.conn = pymysql.connect(db=self.db, user=self.user, passwd=self.passwd,host=self.host)
		self.c = self.conn.cursor()

	def getProgress(self, name):
		"""
		Fetch progress from user
		"""
		self.c.execute("SELECT prog FROM users WHERE name={}".format('"' + name + '"'))
		try:
			return self.c.fetchone()[0]
		except TypeError:
			return 'TypeError Caught: User does not exist. APIc Fail'
	
	def dumpProgress(self, name, progress):
		"""
		DOES NOT WORK -- Save progress from user
		"""
		pass

	def checkCredentials(self, name, passwd):
		"""
		Check User login information against database
		TODO hash passwords!!
		"""
		self.c.execute("SELECT pass FROM users WHERE name={}".format('"' + name + '"'))
		try:
			out = self.c.fetchone()[0]
			return passwd == out
		except TypeError:
			return 'TypeError Caught: User does not exist. APIc Fail'

	def test(self):
		return 'oof'