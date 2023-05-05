class ExchangePeriod():

    MIN_DAYS = 5
    MIN_TRADES = 10
    MIN_VOLUME_RATE = 0.1

    def __init__(self, initial_volume, count_deals, trading_volume, count_days):
        self.initial_volume = initial_volume
        self.count_deals = count_deals
        self.trading_volume = trading_volume
        self.count_days = count_days

    def get_activity(self):
        conditions_met = 0
        if(self.count_days >= self.MIN_DAYS): conditions_met += 1
        if(self.count_deals >= self.MIN_TRADES): conditions_met += 1
        if(self.get_volume_rate() >= self.MIN_VOLUME_RATE): conditions_met += 1

        if conditions_met == 3:
            return 'ACTIVE'
        elif conditions_met == 2:
            return 'LOW_ACTIVE'
        else:
            return 'INACTIVE'

    def get_volume_rate(self):
        return round(self.trading_volume / self.initial_volume * 100, 2)