from lib.basehandler import BaseWebSocket


__author__ = 'faisal'


class Commands(BaseWebSocket):

    def add(self, a, b):

        return a + b
