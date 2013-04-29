# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Defines the Application.
"""

from services.baseapp import set_app
from services.wsgiauth import Authentication
from syncwhoami.controllers import WhoamiController

urls = [('GET', '/', 'whoami', 'index'),
        ('GET', '/whoami', 'whoami', 'get_user_details', {'auth': True})]


controllers = {
    'whoami':  WhoamiController
}


class WhoamiAuthentication(Authentication):
    """Authentication wrapper to automatically load 'syncNode' property.

    This is a quick monkey-patch to force the baseapp authentication machinery
    into always loading the 'syncNode' attribute of a user, even if we're not
    doing full-on node checking.
    """

    def __init__(self, config):
        super(WhoamiAuthentication, self).__init__(config)
        self._orig_authenticate_user = self.backend.authenticate_user
        self.backend.authenticate_user = self._authenticate_user

    def _authenticate_user(self, user, credentials, attrs=None):
        if not attrs:
            attrs = ['syncNode']
        else:
            attrs = list(attrs) + ['syncNode']
        return self._orig_authenticate_user(user, credentials, attrs)


make_app = set_app(urls, controllers, auth_class=WhoamiAuthentication)
