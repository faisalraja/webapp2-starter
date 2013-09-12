import logging
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException

ERROR_LOGIN = 'Login Error'
TYPE_ERROR = 'error'


# Sample json rpc
class ApiHandler(RpcHandler):

    def user_id(self):

        return self.session.get('user_id', 0)

    def login(self):

        self.session['user_id'] = 1
        return self.session['user_id']

    def logout(self):
        if self.is_logged_in():
            del self.session['user_id']
            return True
        return False

    def is_logged_in(self):

        return self.session.get('user_id', 0) != 0

    def hello(self, world, limit=1):

        return [world for i in range(limit)]

    def sample_error(self):
        # this is good for any types of errors
        raise ServerException('Just a sample error')