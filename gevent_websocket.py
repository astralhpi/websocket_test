from gevent import monkey
monkey.patch_all()

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource


class EchoApplication(WebSocketApplication):
    def on_message(self, message):
        try:
            self.ws.send(message)
        except:
            pass


WebSocketServer(
    ('0.0.0.0', 8000),
    Resource({
        '^/echo': EchoApplication
    }),
    debug=False
).serve_forever()
