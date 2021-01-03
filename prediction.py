import requests

# from colored import fg, attr
import matplotlib.pyplot as plt

# import pandas as pd
# import numpy as np
import datetime as dt


class SMAFinder:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None

    def load_data(self, day=5):
        if self.data is None:
            url = (
                "https://query1.finance.yahoo.com/v8/finance/chart/"
                + self.symbol
                + ".NS?region=IN&lang=en-IN&includePrePost=false&interval=15m&range="
                + str(day)
                + "d&corsDomain=in.finance.yahoo.com&.tsrc=finance"
            )
            resp = requests.get(url).json()
            closing_vals = resp["chart"]["result"][0]["indicators"]["quote"][0]["close"]
            self.data = closing_vals
        # remove null values from data
        valid_data = []
        for d in self.data:
            if d is not None:
                valid_data.append(d)
        self.data = valid_data
        return {"data": self.data}

    def smart_sma(self, window):
        d = self.load_data()
        data = d["data"]
        valid_points = data[window:]
        sma_points = []

        # print(data)
        for idx, p in enumerate(valid_points):
            sma_data = data[idx + 1 : idx + window + 1]
            sma_points.append(sum(sma_data) / window)
        # print(sma_points)
        return sma_points

    def smart_ema(self, window):
        d = self.load_data()
        data = d["data"]
        valid_points = data[window:]
        ema0 = sum(data[:window]) / window
        ema_points = []
        for p in valid_points:
            ema = (p - ema0) * (2 / (window + 1)) + ema0
            ema0 = ema
            ema_points.append(ema)
        # print(ema_points)
        return ema_points


if __name__ == "__main__":
    # d = load_data('SBIN', day15)
    # # calculate_simple_avarages(d['dat'], window_size, d['timestamps'])
    # calculate_sma(d, 5)
    sf = SMAFinder("SBIN")
    # sf.sma(50)
    # sf.sma(30)
    # sf.sma(60)
    # sf.sma(70)
    # sf.smart_sma(10)
    # sf.smart_ema(10)
