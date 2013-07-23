"""
This is designed more for backend developers building quick prototypes
If you want to optimize your frontend you should probably start with
using less and having a script the merge and compress them
"""
import logging
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
import webapp2
import config
import routes
from web import errors
from lib import basehandler

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

# Static File Serving
static_app = StaticURLParser("static/")

# Check static files first then fallback
application = Cascade([static_app, app])

if __name__ == '__main__' and basehandler.IS_DEV:
    import paste.reloader as reloader
    reloader.install(10)

    from paste.translogger import TransLogger
    application = TransLogger(application, logger_name=None)

    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port='8080')