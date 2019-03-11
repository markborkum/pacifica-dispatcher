#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the dispatcher module."""
from unittest import TestCase
from pacifica.dispatcher import Dispatcher


class TestDispatcher(TestCase):
    """Test the dispatcher class."""

    def test_add(self):
        """Test the add method in dispatcher class."""
        self.assertEqual(Dispatcher().add('123', 'abc'),
                         '123abc', 'sum of strings should work')
        self.assertEqual(Dispatcher().add(123, 456), 579,
                         'sum of integers should work')

    def test_mul(self):
        """Test the mul method in dispatcher class."""
        self.assertEqual(Dispatcher().mul('a', 4), 'aaaa',
                         'multiply of string and number should work')
        self.assertEqual(Dispatcher().mul(2, 3), 6,
                         'multiply of two integers should work')
