import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
import json
from tornado.options import define, options
from algo import subset

define('num_teams', default=2, help='Number of teams')
define('num_per_team', default=5, help='Number of players per team')

class Match(object):
	num_teams = options.num_teams
	num_per_team = options.num_per_team
	callbacks = []
	players = {}

	def register(self, callback):
		self.callbacks.append(callback)

	def unregister(self, callback):
		self.callbacks.remove(callback)

	def add_players(self, num_players, team_name):
		self.players[team_name] = int(num_players)
		matches, remaining_players = subset.get_n_subsets(self.num_teams, \
														  list(self.players.values()), \
														  self.num_per_team)
		final_result = []
		for k in matches:
			if k == None:
				return

		for k in matches:
			group = {}
			for j in k:
				for name, ps in self.players.items():
					if ps == j:
						group[name] = ps
						del self.players[name]
						break

			final_result.append(group)

		self.notify_all(final_result)

	def remove_players(self, team_name):
		del self.players[team_name]

	def notify_all(self, matches):
		for callback in self.callbacks:
			callback(matches)


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

	def post(self):
		action = self.get_argument('action')
		team_name = self.get_argument('team_name')
		num_players = self.get_argument('num_players', default=None)

		if (not action or not team_name) or \
			(action == 'add' and not num_players):
			self.set_status(400)
			return

		if action == 'add':
			self.application.match.add_players(num_players, team_name)
			self.write(json.dumps("{status: success}"))
		elif action == 'remove':
			self.application.match.remove_players(team_name)
			self.write(json.dumps("{status: success}"))
		else:
			self.set_status(400)


class SocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		self.application.match.register(self.callback)

	def on_close(self):
		self.application.match.unregister(self.callback)

	def on_message(self):
		pass

	def callback(self, matches):
		self.write_message(json.dumps(matches))


class Application(tornado.web.Application):
	def __init__(self):
		self.match = Match()

		handlers = [
			(r'/', IndexHandler),
			(r'/socket', SocketHandler)
		]

		settings = {
			'template_path': 'templates',
			'static_path': 'static'
		}

		tornado.web.Application.__init__(self, handlers, \
										 debug=True, **settings)


if __name__ == '__main__':
	tornado.options.parse_command_line()

	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()