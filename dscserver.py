import twisted
from twisted.web import server, resource, websocket
from twisted.internet import reactor
from txZMQ import ZmqEndpoint, ZmqFactory, ZmqPubConnection, ZmqSubConnection

import redis

rediscli = redis.Redis()
zf = ZmqFactory()

class Chatter(object):
	def __init__(self, topic='chatter', port=9000):
		method = 'bind'
		self.port = port
		endpoint = 'epgm://0.0.0.0:%s' % port
		e = ZmqEndpoint(method, endpoint)
		self.pub_socket = ZmqPubConnection(zf, e)
	
	def get_port():
		return self.port

	def pub(msg):
		self.pub_socket.publish(msg)

class DSCUser(object):
	def __init__(self, transport, chatter):
		self.transport = transport
		self.chatter = chatter
		self.identify()
		method = 'connect'
		self.port = port
		endpoint = 'epgm://127.0.0.1:%s' % port
		e = ZmqEndpoint(method, endpoint)
		self.sub_socket = ZmqSubConnection(zf, e)
		self.sub_socket.gotMessage = self.sub
	
	def identify(self):
		identify_message = json.dumps({'type': 'identify', 'body': DSCUser.userid})
		self.transport.write(identify_message)

	def sub(self, msg):
		self.transport.write(msg)

	def __str__(self):
		return 'hello from {0}'.format(1)


class DSCWebSocketHandler(twisted.web.websocket.WebSocketHandler):
	def __init__(self, transport, dscusers):
		twisted.web.websocket.WebSocketHandler.__init__(self, transport)
		
		self.dscuser = DSCUser(self.transport)
		rediscli.lpush('dscusers', self.dscuser)
		

	def frameReceived(self, frame):
		msg = json.loads(frame)

		if msg['type'] == 'vote':
			tally = rediscli.inc('votetally', int(msg['body']))
			self.chatter.pub(json.dumps({'type': 'votetally',
				'body': tally}))
		elif msg['type'] == 'chatmsg':
			self.chatter.pub(msg)

class DSCFrontend(twisted.web.resource.Resource):
	isLeaf = True
	def __init__(self):
		f = open('./dscfront.html', 'r')
		self.html_response = f.read()
		f.close()
		
	def render_GET(self, request):
		return self.html_response


site = server.Site(DSCFrontend())
root = twisted.web.static.File('.')
websock = twisted.web.websocket.WebSocketSite(root)
websock.addHandler('/websocket', DSCWebSocketHandler())
reactor.listenTCP(8080, site)
reactor.run()
