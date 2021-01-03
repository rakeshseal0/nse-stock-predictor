import requests
# from colored import fg, attr
import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
import datetime as dt



class SMAFinder():
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        self.timestamps = None
    def load_data(self, day=5):
        if self.data is None:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/"  + self.symbol+ ".NS?region=IN&lang=en-IN&includePrePost=false&interval=15m&range=" + str(day) +"d&corsDomain=in.finance.yahoo.com&.tsrc=finance"
            resp = requests.get(url).json()
            closing_vals = resp["chart"]["result"][0]["indicators"]["quote"][0]["close"]
            timestamps = resp["chart"]["result"][0]["timestamp"]
            self.data = closing_vals
            self.timestamps = timestamps
        return ({'data': self.data, 'Date': self.timestamps})

    # def sma(self, window):
    #     d = self.load_data()
    #     #taking last N data for calculating SMA
    #     d['data'] = d['data'][-1*(window):]
    #     filtered_data = []
    #     timestamp_of_sma = None
    #     for idx,dd in enumerate(d['data']):
    #         if dd is not None:
    #             filtered_data.append(dd)
    #     #we are calculating sma for last date
    #     timestamp_of_sma = d['Date'][-1]

    #     data_sum = sum(filtered_data)
    #     sma = data_sum/len(filtered_data)

    #     print('sma_' + str(len(filtered_data)), sma, dt.datetime.fromtimestamp(int(timestamp_of_sma)))

    def smart_sma(self, window):
        d = self.load_data()
        data = d['data']
        valid_points = data[window:]
        sma_points = []

        # print(data)
        for idx,p in enumerate(valid_points):
            sma_data = data[idx+1:idx+window+1]
            sma_points.append(sum(sma_data)/window)
        return sma_points
        
            
        


if __name__ == "__main__":
    # d = load_data('SBIN', day15)
    # # calculate_simple_avarages(d['dat'], window_size, d['timestamps'])
    # calculate_sma(d, 5)
    sf = SMAFinder('SBIN')
    # sf.sma(50)
    # sf.sma(30)
    # sf.sma(60)
    # sf.sma(70)
    sf.smart_sma(10)
