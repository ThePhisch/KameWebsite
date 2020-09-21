from bottle import route, run, template, request
import bottle as b
import api

salt = 69
skey = 'skey'
TTL = 3600


a = api.Connector()
loggedOnCodes = {}

def setLanguage(req):
	"""
	Set language depending on (in order of importance, most->least important):
	* recent choice to change/set language
	* previous choice to set language (read from cookie)
	* HTTP headers (accept-language)
	"""
	currentLang = ""
	if req.query.currentLang.strip() != "":
		currentLang = str(req.query.currentLang.strip())
		b.response.set_cookie('currentLang', currentLang)
	elif req.get_cookie('currentLang') != "":
		currentLang = req.get_cookie('currentLang')
	else:
		if req.headers.get('Accept-Language')[:2] == 'en':
			currentLang = 'en'
		else:
			currentLang = 'de'
	return currentLang

def setCookieForLogon(uName):
	cookieValue = str.encode(str(salt * b.time.time()) + uName)
	hashedCookieValue = b.hashlib.sha224(cookieValue).hexdigest()
	b.response.set_cookie('logged_on', hashedCookieValue, secret=skey, maxage=TTL)
	loggedOnCodes[hashedCookieValue] = (int(b.time.time()), uName)


@b.route("/", method=['GET', 'POST'])
def index():
	p = api.Package(currentLang=setLanguage(b.request))
	logOnCookie = b.request.get_cookie('logged_on', secret=skey)
	if logOnCookie:
		# A cookie exists
		if logOnCookie in loggedOnCodes:
			# Cookie has been found in array
			if b.request.query.get('logout'):
				del loggedOnCodes[logOnCookie]
				b.response.delete_cookie('logged_on')
				return template('index', p=p)
			elif b.time.time() - loggedOnCodes[logOnCookie][0] < TTL:
				# Successful entry with old cookie
				p.uName = loggedOnCodes[logOnCookie][1]
				p.loggedOn = True
				return template('index', p=p)
			else:
				# Fail because cookie has timed out
				del loggedOnCodes[logOnCookie]
				b.response.delete_cookie('logged_on')
				p.cookieTimeout = True
				return template('index', p=p)
		else:
			# Cookie has not been found: malicious or cookie timed out
			p.cookieTimeout = True
			b.response.delete_cookie('logged_on')
			return template('index', p=p)
	elif b.request.forms.get('username') and b.request.forms.get('password'):
		# An attempt at logging on has been made
		if a.checkCredentials(b.request.forms.get('username'), b.request.forms.get('password')):
			# Successfully logged on
			p.uName = b.request.forms.username
			p.loggedOn = True
			setCookieForLogon(p.uName)
			return template('index', p=p)
		else:
			# Fail at logging on
			p.loginFail = True
			return template('index', p=p)
	else:
		# No attempt at logging on, no cookie, serve default site
		return template('index', p=p)

@route('/xapi')
def xapi():
	if b.request.GET.apiName.strip() != "":
		name = b.request.GET.apiName.strip()
		return a.getProgress(name)
	else:
		return 'APIc Fail'



@route('/static/<filename>')
def server_static(filename):
	return b.static_file(filename, root='./static')

@route('/game/<filename>')
def server_game(filename):
	return b.static_file(filename, root='./game')

if __name__ == '__main__':
	run(host='localhost', reloader=True, debug=True)

app = b.default_app()