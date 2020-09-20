from bottle import route, run, template, request
import bottle as b

@route("/")
def index():
	if b.request.GET.currentLang.strip() != "":
		currentLang = str(b.request.GET.currentLang.strip())
		b.response.set_cookie('currentLang', currentLang)
	elif b.request.get_cookie('currentLang') != "":
		currentLang = b.request.get_cookie('currentLang')
	else:
		if b.request.headers.get('Accept-Language')[:2] == 'en':
			currentLang = 'en'
		else:
			currentLang = 'de'
	return template('index', currentLang=currentLang)

@route('/static/<filename>')
def server_static(filename):
	return b.static_file(filename, root='./static')

@route('/game/<filename>')
def server_game(filename):
	return b.static_file(filename, root='./game')

if __name__ == '__main__':
	run(host='localhost', reloader=True, debug=True)

app = b.default_app()