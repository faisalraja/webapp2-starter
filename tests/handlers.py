import unittest
import webapp2
from webapp2_extras import jinja2
import wsgi

__author__ = 'faisal'

# Correct templates path
jinja2.default_config['template_path'] = '../templates'


class AppTest(unittest.TestCase):

    def testHomeHandler(self):

        request = webapp2.Request.blank('/')

        # Get Test
        response = request.get_response(wsgi.application)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>Webapp2 Starter</title>', response.body)

        # Check if good status code
        self.assertEqual(response.status_code, 200)