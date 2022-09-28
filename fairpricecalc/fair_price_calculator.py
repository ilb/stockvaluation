import math
from exchange_data_provider import ExchangeDataProvider
from date_utils import DateUtils

class FairPriceCalculator():

    MIN_DAYS = 5
    MIN_TRADES = 10
    MIN_VOLUME_RATE = 0.1

    def __init__(self, ticker):
        self.ticker = ticker

    def calculate(self, date):
        '''
        Returns list with calculated data about ticker in
        curtain date: is active, deals, volume rate, is active, fair price.
        '''
        provider = ExchangeDataProvider(date, self.ticker)
        date_utils = DateUtils()

        initial_volume, isin, market_data = provider.get_exchange_data()
        count_deals, trading_volume, count_days, weighted_average \
                            = self._get_merged_values(market_data)

        volume_rate = round(trading_volume / initial_volume * 100, 2)

        # If ticker is active, fair price equals:
        # weighted average (of last trading day) * 10
        # else equals 0
        is_active = self._check_is_active(count_days, count_deals, volume_rate)
        if is_active:
            last_average_index = len(market_data) - 1
            fair_price = weighted_average * 10
        else:
            fair_price = 0

        return {'active': is_active, 'fairPrice': round(fair_price, 2),
                'countDays': count_days, 'countDeals': count_deals,
                'tradingVolume': volume_rate, 'initialVolume': initial_volume,
                'isin': isin,
                'date': date_utils.get_end_date(date),
                'marketData':market_data}

    def _get_merged_values(self, market_data):
        ''' Gets list with market data of each trading day
        and merge values: deals, volume, days, weighted average
        '''
        count_deals = 0
        trading_volume = 0
        count_days = 0
        weighted_average = 0

        for data in market_data:
            count_deals += data['countDeals']
            if data['tradingVolume'] > 0 and not math.isnan(data['weightedAverage']):
                trading_volume += data['tradingVolume'] / (data['weightedAverage'] * 10)
            if data['countDeals'] > 0:
                count_days += 1
            if not math.isnan(data['weightedAverage']):
                weighted_average = data['weightedAverage']
            else:
                data['weightedAverage'] = 0

        return count_deals, trading_volume, count_days, weighted_average

    def _check_is_active(self, days, deals, rate):
        return days >= self.MIN_DAYS \
                and deals >= self.MIN_TRADES \
                and rate >= self.MIN_VOLUME_RATE
