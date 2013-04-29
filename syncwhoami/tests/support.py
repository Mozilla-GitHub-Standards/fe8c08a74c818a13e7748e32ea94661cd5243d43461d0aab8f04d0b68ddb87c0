# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import services.tests.support


def initenv(config=None, **env_args):
    """Reads the config file and instantiates an auth and a storage.
    """
    env_args.setdefault('ini_dir', os.path.dirname(__file__))
    return services.tests.support.initenv(config, **env_args)


def cleanupenv(config=None, **env_args):
    env_args.setdefault('ini_dir', os.path.dirname(__file__))
    return services.tests.support.cleanupenv(config, **env_args)
