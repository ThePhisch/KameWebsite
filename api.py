import pymysql
import hashlib
import time

class SQL_Basis():
	"""
	Class to connect to MariaDB
	Provides helper functions and especially an abstraction layer so database does not
	have to be opened to remote access.
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
		self.conn.autocommit(True)
		self.c = self.conn.cursor()

class Connector(SQL_Basis):
	"""
	Interface using SQL_Basis for the game
	"""
	def getProgress(self, name):
		"""
		Fetch progress from user
		"""
		self.c.execute("SELECT SQL_NO_CACHE prog FROM users WHERE name=%s", (name,))
		try:
			return self.c.fetchone()[0]
		except TypeError:
			return 'TypeError Caught: User does not exist. APIc Fail'
	
	def dumpProgress(self, name, progress):
		"""
		Save progress from user
		"""
		self.c.execute("UPDATE users SET prog='%s' WHERE name='%s'" % (progress, name))

	def checkCredentials(self, name, passwd):
		"""
		Check User login information against database
		"""
		self.c.execute("SELECT pass FROM users WHERE name=%s", (name,))
		out = self.c.fetchone()
		if out:
			return hashlib.sha224(str.encode(passwd)).hexdigest() == out[0]
		else:
			return False
		

	def test(self):
		return 'oof'

class Package():
	"""
	Class to send information to templates
	Has built-in default values
	"""
	def __init__(self, **kwargs):
		self.setDefault()
		self.__dict__.update(kwargs)

	def setDefault(self):
		self.loginFail = False
		self.uName = ""
		self.currentLang = 'de'
		self.cookieTimeout = False
		self.loggedOn = False
		self.passwordChanged = False
		self.passwordChangeError = False
		self.passwordMismatch = False

class Logger(SQL_Basis):
	"""
	Interface using SQL_Basis for the login
	"""
	def __init__(self, salt=69, skey='skey', ttl=3600):
		super().__init__()
		self.salt = salt
		self.skey = skey
		self.ttl = ttl

	def setCookieForLogon(self, uName):
		cookieValue = str.encode(str(self.salt * time.time()) + uName)
		hashedCookieValue = hashlib.sha224(cookieValue).hexdigest()
		vals = (hashedCookieValue, uName, int(time.time()))
		# self.loggedOnCodes[hashedCookieValue] = (int(time.time()), uName)
		self.c.execute('INSERT INTO sessions (cookieValue, cookieName, cookieTime) VALUES ("%s", "%s", %i)' % vals)
		return hashedCookieValue

	def checkExists(self, cookieValueToProve):
		self.c.execute('SELECT cookieName, cookieTime FROM sessions WHERE cookieValue=%s', (cookieValueToProve,)) 
		return self.c.fetchone() # returns tuple (uName : String, time : int) or None

	def removeEntry(self, cookieValueToDelete):
		self.c.execute('DELETE FROM sessions WHERE cookieValue="%s"' % cookieValueToDelete)

class Usermethods(SQL_Basis):
	"""
	Interface using SQL_Basis for the user/admin related stuff
	"""
	def __init__(self):
		super().__init__()

	def changePassword(self, uName, newPassword):
		vals = (hashlib.sha224(str.encode(newPassword)).hexdigest(), uName)
		self.c.execute('UPDATE users SET pass=%s WHERE name=%s', vals)

	def checkCredentials(self, name, passwd):
		"""
		Check User login information against database
		"""
		self.c.execute("SELECT pass FROM users WHERE name=%s", (name,))
		out = self.c.fetchone()
		if out:
			return hashlib.sha224(str.encode(passwd)).hexdigest() == out[0]
		else:
			return False