#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import unittest
from unittest import mock
import sys

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_PATH)

from core.services import RemovalService, UploadService

class RemovalServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.removal_service = RemovalService()

    @mock.patch('core.services.os.remove')
    @mock.patch('core.services.os.path.isfile')
    def test_rm_pass(self, mock_path, mock_os):
        filename = 'test'
        mock_path.return_value = True
        self.removal_service.rm(filename)
        self.assertTrue(mock_os.called)
        mock_path.assert_called_once_with(filename)

    @mock.patch('core.services.os.remove')
    @mock.patch('core.services.os.path.isfile')
    def test_rm_fail(self,mock_path, mock_os):
        filename = 'test'
        mock_path.return_value = False
        self.removal_service.rm(filename)
        self.assertFalse(mock_os.called)
        mock_path.assert_called_once_with(filename)

class UploadServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.removal_service = RemovalService()
        self.upload_service = UploadService(self.removal_service)

    @mock.patch.object(RemovalService, 'rm')
    def test_upload_complete(self, mock_rm):
        filename = 'test'
        self.upload_service.upload_complete(filename)
        mock_rm.assert_called_once_with(filename)
