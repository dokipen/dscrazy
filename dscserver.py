from twisted.web import server, resource
from twisted.internet import reactor

import redis


class DSCUser(object):
	def __init__(self, transport):
		self.transport = transport
	
	def identify(self):
		identify_message = json.dumps({'user': DSCUser.userid})
		self.transport.write(identify_message)

class DSCWebSocketHandler(twisted.web.websocket.WebSocketHandler):
	def __init__(self, transport):
		twisted.web.websocket.WebSocketHandler.__init__(self, transport)
		self.dscuser = DSCUser(self.transport)


	
