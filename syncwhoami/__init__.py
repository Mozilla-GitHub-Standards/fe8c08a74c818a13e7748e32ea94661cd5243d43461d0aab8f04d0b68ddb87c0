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

make_app = set_app(urls, controllers, auth_class=Authentication)
