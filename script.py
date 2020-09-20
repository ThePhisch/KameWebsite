from bottle import route, run, template, request
import bottle as b

@route("/")
def index():
	# return template('transtest')
	return template('index')

@route('/static/<filename>')
def server_static(filename):
	return b.static_file(filename, root='./static')

@route('/game/<filename>')
def server_game(filename):
	return b.static_file(filename, root='./game')

if __name__ == '__main__':
	run(host='localhost', reloader=True, debug=True)

app = b.default_app()