import unittest
import tempfile
import getpass
import glob as gl

from pandas import DatetimeIndex
from unittest import mock

from ..file_browser import FileBrowser

BASE_FILE_PATH = tempfile.gettempdir() + '/stockvaluation/' + \
                     getpass.getuser()

class TestFileBrowser(unittest.TestCase):

    TRUE_OUTPUT_LENGTH = 22
    TEST_DATE = '2019-03-29'
    TRUE_OUTPUT_VOLUME_FILE = 'fairpricevalc/test/volume.xhtml'

    def test_get_file(self):
        browser = FileBrowser(self.TEST_DATE)
        volume_file, exchange_files = browser.get_files()
        self.assertTrue(gl.glob(volume_file)[0].find('xhtml') > 0)
        self.assertEqual(len(exchange_files), self.TRUE_OUTPUT_LENGTH)