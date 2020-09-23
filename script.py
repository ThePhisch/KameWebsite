from bottle import route, run, template, request
import bottle as b
import api


a = api.Connector()
l = api.Logger()
u = api.Usermethods()

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


@b.route("/", method=['GET', 'POST'])
def index():
	p = api.Package(currentLang=setLanguage(b.request))
	logOnCookie = b.request.get_cookie('logged_on', secret=l.skey)
	if logOnCookie:
		# A cookie exists
		logTuple = l.checkExists(logOnCookie) # TODO change this to two variables
		if logTuple:
			# Cookie has been found in array
			if b.request.query.get('logout'):
				# Log out
				l.removeEntry(logOnCookie)
				b.response.delete_cookie('logged_on')
				return template('index', p=p)
			elif b.time.time() - logTuple[1] < l.ttl:
				# Successful entry with old cookie
				p.uName = logTuple[0]
				p.loggedOn = True
				if b.request.forms.get('changePassword'):
					if b.request.forms.get('newPassword') == b.request.forms.get('newPasswordConfirm'):
						if u.checkCredentials(logTuple[0], b.request.forms.get('oldPassword')):
							u.changePassword(logTuple[0], b.request.forms.get('newPassword'))
							p.passwordChanged = True
						else:
							p.passwordChangeError = True
					else:
						p.passwordMismatch = True
				return template('index', p=p)
			else:
				# Fail because cookie has timed out
				l.removeEntry(logOnCookie)
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
			hashedCookieValue = l.setCookieForLogon(p.uName)
			b.response.set_cookie('logged_on', hashedCookieValue, secret=l.skey, maxage=l.ttl)
			return template('index', p=p)
		else:
			# Fail at logging on
			p.loginFail = True
			return template('index', p=p)
	else:
		# No attempt at logging on, no cookie, serve default site
		return template('index', p=p)

@route('/xapi', method=['GET', 'POST'])
def xapi():
	apiName = b.request.GET.apiName.strip()
	apiInput = b.request.GET.apiInput.strip()
	apiProg = b.request.POST.apiProg
	if apiName != "" and apiInput != "":
		if apiInput == "0":
			# Return progress
			return a.getProgress(apiName)
		elif apiInput == "1":
			# Update progress with input
			a.dumpProgress(apiName, apiProg)
			return apiProg
		else:
			return 'bad parameter'
		
	else:
		return 'APIc Fail'

@route('/jstest')
def jstest():
	return template('./game/k.tpl', col=b.request.query.get('col'))


@route('/static/<filename>')
def server_static(filename):
	return b.static_file(filename, root='./static')

@route('/game/<filename>')
def server_game(filename):
	return b.static_file(filename, root='./game')

if __name__ == '__main__':
	run(host='localhost', reloader=True, debug=True)

app = b.default_app()