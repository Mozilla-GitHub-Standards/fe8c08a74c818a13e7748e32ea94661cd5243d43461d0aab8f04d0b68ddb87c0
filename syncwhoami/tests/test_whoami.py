
import os
import base64
import unittest

from webtest import TestApp

from services.user import User
from syncwhoami import make_app
from syncwhoami.tests.support import initenv, cleanupenv


def get_auth_header(username, password):
    return "Basic " + base64.encodestring('%s:%s' % (username, password))


class TestWsgiApp(unittest.TestCase):

    def setUp(self):
        # load the app configured for testing
        self.appdir, self.config, self.auth = initenv()
        self.app = TestApp(make_app(self.config))

    def tearDown(self):
        # don't leave cef logs from failed login attempts
        cef_logs = os.path.join(self.appdir, 'test_cef.log')
        if os.path.exists(cef_logs):
            os.remove(cef_logs)

        # Clear out the database.
        if "sqlite" not in self.auth.sqluri:
            self.auth._engine.execute('truncate user')

        # Remove any sqlite db files that we created.
        cleanupenv()

    def _create_user(self, username, password, email=None, syncNode=None):
        """Create a user in the DB, and return the user object."""
        if not email:
            email = 'test@example.com'
        if not syncNode:
            syncNode = 'http://sync1.example.com'
        self.auth.create_user(username, password, email)
        user = self.auth.get_user_info(User(username), ['syncNode'])
        self.auth.admin_update_field(user, 'syncNode', syncNode)
        return user

    def test_it_works_page(self):
        r = self.app.get('/')
        self.assertEqual(r.body, 'It Works!')

    def test_successful_authentication(self):
        username = 'test1'
        password = 'testtesttest'
        user = self._create_user(username, password)
        r = self.app.get('/whoami', headers={
            'Authorization': get_auth_header(username, password)
        })
        self.assertEqual(r.json, {
            'userid': user['userid'],
            'syncNode': user['syncNode'],
        })

    def test_unsuccessful_authentication(self):
        username = 'test1'
        password = 'testtesttest'
        self._create_user(username, password)
        # No authz header => 401
        self.app.get('/whoami', headers={}, status=401)
        # Bad password => 401
        self.app.get('/whoami', headers={
            'Authorization': get_auth_header(username, 'badpassword')
        }, status=401)
        # Bad username => 401
        self.app.get('/whoami', headers={
            'Authorization': get_auth_header('evildoer', password)
        }, status=401)
