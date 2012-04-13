# Copyright (c) 2009 Twisted Matrix Laboratories.
# See LICENSE for details.

"""
WebSocket example: echo service.

This creates a simple echo WebSocket example, accessible on
http://localhost:8080/ with a browser supporting WebSocket.
"""

import sys

from twisted.python import log
from twisted.internet import reactor
from twisted.web.websocket import WebSocketHandler, WebSocketSite
from twisted.web.resource import Resource



class Echohandler(WebSocketHandler):

    def frameReceived(self, frame):
        log.msg("Received frame '%s'" % frame)
        self.transport.write(frame)



class ExampleResource(Resource):

    def getChildWithDefault(self, path, request):
        if not path:
            return self
        return Resource.getChildWithDefault(self, path, request)


    def render_GET(self, request):
        return """<html>
<head>
    <title>WebSocket example: echo service</title>
</head>
<body>
<h1>WebSocket example: echo service</h1>
<script type="text/javascript">
    var ws = new WebSocket("ws://127.0.0.1:8080/ws/echo");
    ws.onmessage = function(evt) {
        var data = evt.data;
        var target = document.getElementById("received");
        target.value = target.value + data;
    };
    window.send_data = function() {
        ws.send(document.getElementById("send_input").value);
    };
</script>
<form>
    <label for="send_input">Text to send</label>
    <input type="text" name="send_input" id="send_input"/>
    <input type="submit" name="send_submit" id="send_submit" value="Send"
    onclick="send_data(); return false"/>
    <br />
    <label for="received">Received text</label>
    <textarea name="received" id="received"></textarea>
</form>
</body>
</html>"""



def main():
    log.startLogging(sys.stdout)
    root = ExampleResource()
    site = WebSocketSite(root)
    site.addHandler("/ws/echo", Echohandler)
    reactor.listenTCP(8080, site)
    reactor.run()



if __name__ == "__main__":
    main()
