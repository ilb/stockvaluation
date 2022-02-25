from file_browser import FileBrowser
from dataframe_parser import DataFrameParser
from datetime import date, timedelta

import pandas as pd
import sys


class ExchangeDataProvider():


    def __init__(self, date, ticker):
        self.ticker = ticker
        self.date = date

    def get_exchange_data(self):
        '''
        Returns initial volume and market data of certain ticker and date
        '''
        browser = FileBrowser(self.date)
        parser = DataFrameParser(self.ticker)
        volume_file, exchange_files = browser.get_files()

        volume_df = parser.parse_volume_file(volume_file)
        exchange_df = parser.parse_exchange_files(exchange_files)

        market_data = []
        for index, row in exchange_df.iterrows():
            market_data.append({
                "countDeals":self._check_dtype_int(row['NumberOfTrades']),
                "tradingVolume":self._check_dtype_float(row['Volume']),
                "weightedAverage":self._check_dtype_float(row['WeightedAverage'])
                })

        initial_volume = self._get_initial_volume(volume_df)

        return initial_volume, market_data

    def _get_initial_volume(self, df):
        '''
        Process a dataframe and returns a initial
        volume of the certain paper
        '''
        df = df.loc[df[0] == self.ticker]

        if isinstance(df[1], pd.Series):
            return int(df[1].values[0])
        else:
            return int(df[1])

    def _check_dtype_float(self, value):
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return float(value)
        else:
            return float(value.replace(',','.'))

    def _check_dtype_int(self, value):
        if isinstance(value, int):
            return value
        else:
            return int(value)
