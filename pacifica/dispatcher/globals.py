#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Global configuration options expressed in environment variables."""
from os import getenv
from os.path import expanduser, join

CONFIG_FILE = getenv('DISPATCHER_CONFIG', join(
    expanduser('~'), '.pacifica-dispatcher', 'config.ini'))
CHERRYPY_CONFIG = getenv('DISPATCHER_CPCONFIG', join(
    expanduser('~'), '.pacifica-dispatcher', 'cpconfig.ini'))
