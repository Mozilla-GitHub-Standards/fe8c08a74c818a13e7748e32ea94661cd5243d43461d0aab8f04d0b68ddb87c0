# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Define the Controller.
"""

from services.user import ServicesUser
from services.formatters import text_response, json_response


class WhoamiController(object):

    def __init__(self, app):
        self.app = app
        self.auth = app.auth.backend
        # Fail noisily if not used with a new-style auth backend.
        try:
            is_newstyle_auth = isinstance(self.auth, ServicesUser)
        except Exception:
            is_newstyle_auth = False
        if not is_newstyle_auth:
            msg = "This code will only work with new-style auth backends."\
                  " Please set 'auth.backend' to a class from the"\
                  " services.user package."
            raise ValueError(msg)

    def index(self, request, **kw):
        """Show a simple "It Works!" page at the root."""
        return text_response("It Works!")

    def get_user_details(self, request, **kw):
        """Returns a JSON blob of account details for the current user."""
        return json_response({
            'userid': request.user['userid'],
            'syncNode': request.user['syncNode'],
        })
