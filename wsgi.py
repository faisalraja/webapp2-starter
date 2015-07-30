"""
This is designed more for backend developers building quick prototypes
If you want to optimize your frontend you should probably start with
using less and having a script the merge and compress them
"""
import logging
import webapp2
import config
import routes
from services import sample_websocket
from web import errors
from lib import basehandler, utils
from ws4py.server.geventserver import WSGIServer
from ws4py.server.wsgiutils import WebSocketWSGIApplication
import gevent.monkey
gevent.monkey.patch_all()


app = webapp2.WSGIApplication(debug=basehandler.IS_DEV, config=config.webapp2_config, routes=routes.get_routes())


# defined custom error handlers
class Webapp2HandlerAdapter(webapp2.BaseHandlerAdapter):

    def __call__(self, request, response, exception):
        request.route_args = {
            'exception': exception
        }
        logging.exception(exception)
        handler = self.handler(request, response)

        return handler.get()

app.error_handlers[403] = Webapp2HandlerAdapter(errors.Error403Handler)
app.error_handlers[404] = Webapp2HandlerAdapter(errors.Error404Handler)
app.error_handlers[503] = Webapp2HandlerAdapter(errors.Error503Handler)
app.error_handlers[500] = Webapp2HandlerAdapter(errors.Error500Handler)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    http_server = WSGIServer(('', 8080), app)
    ws_server = WSGIServer(('', 9000), WebSocketWSGIApplication(handler_cls=sample_websocket.Commands))

    greenlets = [
        gevent.spawn(http_server.serve_forever),
        gevent.spawn(utils.background_service),
        gevent.spawn(ws_server.serve_forever)
    ]

    try:
        gevent.joinall(greenlets)
    except KeyboardInterrupt:
        http_server.stop()
        print 'Stopping'
