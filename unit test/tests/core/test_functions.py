#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import os
import sys
from unittest import mock

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_PATH)

from core import functions


class FunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.functions = functions.Functions()

    def test_add_pass(self):
        self.assertEquals(6, self.functions.add(3, 3))

    def test_add_fail(self):
        self.assertNotEquals(12, self.functions.add(2, 8))

    @mock.patch.object(functions.Functions, 'add')
    def test_strange_add_pass(self, mock_add):
        num1 = 2
        num2 = 8
        mock_add.return_value = 10
        self.assertEquals(20, self.functions.strange_add(num1, num2))
        mock_add.assert_called_once_with(num1, num2)

    @mock.patch.object(functions.Functions, 'add')
    def test_strange_add_fail(self, mock_add):
        num1 = 2
        num2 = 8
        mock_add.return_value = 5
        self.assertNotEquals(20, self.functions.strange_add(num1, num2))
        mock_add.assert_called_once_with(num1, num2)
