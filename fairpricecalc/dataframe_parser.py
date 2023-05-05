import pandas as pd

class DataFrameParser():
    
    def __init__(self, ticker):
        self.ticker = ticker
    
    def parse_volume_file(self, file):
        return self._parse_html(file)
    
    def parse_exchange_files(self, market_files):
        ''' 
        Returns a dataframe with the exchange 
        data of curtain paper
        '''
        frames_list = []
        for file in market_files:
            if file != None:
                # Parsing csv and making dataframe with only 
                # certain ticker data 
                df = self._parse_csv(file)
                df = df[df['Code'].isin([self.ticker])]
                if df.empty:
                    continue                    
                frames_list.append(df)

        if len(frames_list) == 0:
            raise NameError('Data for this ticker does not exist: ' + self.ticker)
        return pd.concat(frames_list)
    
    def _parse_csv(self, file):
        return pd.read_csv(file, sep=';')
        
    def _parse_html(self, file):
        return pd.read_html(file)[0]