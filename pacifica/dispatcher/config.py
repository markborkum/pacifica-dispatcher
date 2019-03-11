#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Configuration reading and validation module."""
from configparser import ConfigParser
from .globals import CONFIG_FILE


def get_config():
    """Return the ConfigParser object with defaults set."""
    configparser = ConfigParser({
        'peewee_url': 'sqliteext:///db.sqlite3'
    })
    configparser.add_section('database')
    configparser.read(CONFIG_FILE)
    return configparser
