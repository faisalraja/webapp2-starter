import logging
import mimetypes
import os
from lib.basehandler import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        params = {}
        return self.render_template('main/index.html', **params)


class StaticHandler(BaseHandler):

    def get(self, folder, path):
        full_path = os.path.join(os.path.dirname(__file__), '..', 'static', folder, path)
        if os.path.exists(full_path):
            self.response.headers['Content-Type'] = mimetypes.guess_type(path)[0]
            with open(full_path, 'r') as f:
                return self.response.write(f.read())
        self.abort(404)


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
