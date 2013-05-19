# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Sync Server
#
# The Initial Developer of the Original Code is the Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Tarek Ziade (tarek@mozilla.com)
#   Ryan Kelly (rfkelly@mozilla.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
"""
Load test for the whoami server
"""
import random
import json

from funkload.FunkLoadTestCase import FunkLoadTestCase


class StressTest(FunkLoadTestCase):

    def setUp(self):
        pass

    def _browse(self, url_in, params_in=None, description=None, ok_codes=None,
                method='post', *args, **kwds):
        args = (url_in, params_in, description, ok_codes, method) + args
        self.logi("%s: %s" % (method.upper(), url_in))
        try:
            result = super(StressTest, self)._browse(*args, **kwds)
        except Exception, e:
            self.logi("    FAIL: " + url_in + " " + repr(e))
            raise
        else:
            self.logi("    OK: " + url_in + " " + repr(result))
            return result

    def test_whoami_api(self):
        username = "cuser%i" % random.randint(1, 1000000)
        if random.randint(1, 10) <= 9:
            password = "password"
            self.setOkCodes([200])
        else:
            password = "wrongpassword"
            self.setOkCodes([401])
        self.setBasicAuth(username, password)

        url = "https://whoami.services.mozilla.com/whoami"
        response = self.get(url)
        if response.code == 200:
            assert response.body
            user_data = json.loads(response.body)
            assert "userid" in user_data
            assert "syncNode" in user_data
