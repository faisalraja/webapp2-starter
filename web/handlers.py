import logging
import os
from lib.basehandler import BaseHandler


# Check routes.py to see hot everything is routed here
from models import models


class HomeHandler(BaseHandler):

    def get(self):
        params = {}
        logging.info(os.environ)
        return self.render_template('main/index.html', **params)


class LoginHandler(BaseHandler):

    def get(self):
        # hold referer to redirect back
        referer = self.request.referer or '/'
        if self.request.path not in referer:
            self.session['referer'] = referer

        referer = self.session.get('referer', '/')

        if self.user_id:
            self.redirect(referer)
        else:
            # todo implement your user login here
            self.session['user_id'] = 1
            self.add_message('Logged in successfully')
            self.redirect(str(referer))
        return


class LogoutHandler(BaseHandler):

    def get(self):

        if 'user_id' in self.session:
            del self.session['user_id']

        self.add_message('Logged out successfully')
        self.redirect(self.request.referer or '/')
        return
