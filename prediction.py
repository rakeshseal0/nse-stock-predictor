import requests
import matplotlib.pyplot as plt
import datetime as dt


class SMAFinder:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None

    def load_data(self, day=1):
        if self.data is None:
            url = (
                "https://query1.finance.yahoo.com/v8/finance/chart/"
                + self.symbol
                + ".NS?region=IN&lang=en-IN&includePrePost=false&interval=1m&range="
                + str(day)
                + "d&corsDomain=in.finance.yahoo.com&.tsrc=finance"
            )
            resp = requests.get(url).json()
            closing_vals = resp["chart"]["result"][0]["indicators"]["quote"][0]["close"]
            timestamps = timestamp = resp["chart"]["result"][0]["timestamp"]
            self.timestamps = timestamps
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
    def predict_buy_point(self, small_window_data, large_window_data, timestamps):
        self.timestamps = timestamps[-1*(len(large_window_data)):]
        #data set should be of same length
        datapoints = []
        small_window_data = small_window_data[-1*len(large_window_data):]
        print(len(small_window_data), len(large_window_data), len(timestamps))
        for idx,_ in enumerate(small_window_data):
            try:
                if (small_window_data[idx] < large_window_data[idx]) and (small_window_data[idx+1] >= large_window_data[idx+1]):
                    ts = self.timestamps[idx]
                    datapoints.append([large_window_data[idx], ts])
            except:
                pass
        return (datapoints)

    def predict_sell_point(self, small_window_data, large_window_data, timestamps):
        self.timestamps = timestamps[-1*(len(large_window_data)):]
        #data set should be of same length
        datapoints = []
        small_window_data = small_window_data[-1*len(large_window_data):]
        for idx,_ in enumerate(small_window_data):
            try:
                if (small_window_data[idx] > large_window_data[idx]) and (small_window_data[idx+1] <= large_window_data[idx+1]):
                    ts = self.timestamps[idx]
                    datapoints.append([large_window_data[idx], ts])
            except:
                pass
                # print(idx, len(small_window_data))
        return (datapoints)

                




if __name__ == "__main__":
    # d = load_data('SBIN', day15)
    # # calculate_simple_avarages(d['dat'], window_size, d['timestamps'])
    # calculate_sma(d, 5)
    sf = SMAFinder("SBIN")
    # sf.sma(50)
    # sf.sma(30)
    # sf.sma(60)
    # sf.sma(70)
    sm = sf.smart_sma(20)
    em = sf.smart_ema(10)
    sf.predict_transaction_point(em, sm, sf.timestamps)
