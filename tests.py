import unittest
from flask import Flask
from app import app
import os


class TestCase(unittest.TestCase):

    TESTING = True

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(os.environ['APP_SETTINGS'])
        self.client = app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()


if __name__ == '__main__':
    unittest.main()
