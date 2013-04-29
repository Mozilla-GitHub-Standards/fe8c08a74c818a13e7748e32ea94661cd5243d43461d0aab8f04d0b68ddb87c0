# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup

install_requires = ['Services', 'PasteScript']

entry_points = """
[paste.app_factory]
main = syncwhoami:make_app

[paste.app_install]
main = paste.script.appinstall:Installer
"""

setup(name='SyncWhoami', version="1.0", packages=['syncwhoami'],
      install_requires=install_requires, entry_points=entry_points)
