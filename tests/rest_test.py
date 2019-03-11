#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the rest interface."""
from time import sleep
import requests
import cherrypy
from cherrypy.test import helper
from pacifica.dispatcher.globals import CHERRYPY_CONFIG
from pacifica.dispatcher.orm import database_setup, DispatcherModel
from pacifica.dispatcher.rest import Root, error_page_default


def dispatchermodel_droptables(func):
    """Setup the database and drop it once done."""
    def wrapper(*args, **kwargs):
        """Create the database table."""
        database_setup()
        func(*args, **kwargs)
        DispatcherModel.drop_table()
    return wrapper


class DispatcherCPTest(helper.CPWebCase):
    """Base class for all testing classes."""

    HOST = '127.0.0.1'
    PORT = 8050
    url = 'http://{0}:{1}'.format(HOST, PORT)
    headers = {'content-type': 'application/json'}

    @staticmethod
    def setup_server():
        """Bind tables to in memory db and start service."""
        cherrypy.config.update({'error_page.default': error_page_default})
        cherrypy.config.update(CHERRYPY_CONFIG)
        cherrypy.tree.mount(Root(), '/', CHERRYPY_CONFIG)

    @dispatchermodel_droptables
    def test_default_mul(self):
        """Test a default summation in dispatcher."""
        resp = requests.get('{}/dispatch/mul/2/2'.format(self.url))
        self.assertEqual(resp.status_code, 200)
        uuid = resp.text
        sleep(2)
        resp = requests.get('{}/status/{}'.format(self.url, uuid))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(int(resp.text), 4)

    @dispatchermodel_droptables
    def test_default_sum(self):
        """Test a default summation in dispatcher."""
        resp = requests.get('{}/dispatch/add/2/2'.format(self.url))
        self.assertEqual(resp.status_code, 200)
        uuid = resp.text
        sleep(2)
        resp = requests.get('{}/status/{}'.format(self.url, uuid))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(int(resp.text), 4)

    @dispatchermodel_droptables
    def test_string_mul(self):
        """Test a default summation in dispatcher."""
        resp = requests.get('{}/dispatch/mul/a/2'.format(self.url))
        self.assertEqual(resp.status_code, 200)
        uuid = resp.text
        resp = requests.get('{}/status/{}'.format(self.url, uuid))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, 'aa')

    @dispatchermodel_droptables
    def test_error_sum(self):
        """Test a default summation in dispatcher."""
        resp = requests.get('{}/dispatch/add/2/2/2'.format(self.url))
        self.assertEqual(resp.status_code, 200)
        uuid = resp.text
        resp = requests.get('{}/status/{}'.format(self.url, uuid))
        self.assertEqual(resp.status_code, 404)

    @dispatchermodel_droptables
    def test_error_json(self):
        """Test a default summation in dispatcher."""
        resp = requests.get('{}/status'.format(self.url))
        self.assertEqual(resp.status_code, 500)
