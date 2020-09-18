from bottle import route, run, template
import bottle

@route("/")
def index():
	return template('index')

@route('/game/<filename>')
def server_game_static(filename):
	return bottle.static_file(filename, root='./game')

if __name__ == '__main__':
	run(host='localhost', reloader=True, debug=True)

app = bottle.default_app()
