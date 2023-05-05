import unittest
import pandas as pd
from ..dataframe_parser import DataFrameParser

class TestDataFrameParser(unittest.TestCase):
    
    TEST_VOLUME_FILE = 'fairpricecalc/test/volume.xhtml'
    TEST_EXCHANGE_FILE = ['fairpricecalc/test/test.csv']
    TEST_TICKER = 'ТойотаБ1P2'
    
    def test_parse_volume_file(self):
        parser = DataFrameParser(self.TEST_TICKER)
        self.assertIsInstance(parser.parse_volume_file(self.TEST_VOLUME_FILE), pd.DataFrame)
    
    def test_parse_exchange_file(self):
        parser = DataFrameParser(self.TEST_TICKER)
        self.assertIsInstance(parser.parse_exchange_files(self.TEST_EXCHANGE_FILE), pd.DataFrame)