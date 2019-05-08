import unittest


from stockvaluation.dataframe_parser import DataFrameParser
import stockvaluation.file_browser
from stockvaluation.exchange_data_provider import ExchangeDataProvider


class TestExchangeDataProvider(unittest.TestCase):

    TEST_TICKER = 'ТойотаБ1P2'
    TEST_DATE = '2019-03-29'
    
    def test_get_exchange_data(self):
        provider = ExchangeDataProvider(self.TEST_DATE, self.TEST_TICKER)
        initial_volume, market_data = provider.get_exchange_data()
        self.assertTrue(isinstance(initial_volume, int))
        self.assertTrue(len(market_data) > 0)
        