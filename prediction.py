import requests
# from colored import fg, attr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt



day5 = '5'
day15 = '16'
DATA_STREAM_INTERVAL = 1 #day
window_size = 5


def load_data(symbol, day):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/"  + symbol+ ".NS?region=IN&lang=en-IN&includePrePost=false&interval=" + str(DATA_STREAM_INTERVAL) +  "d&range=" + day +"d&corsDomain=in.finance.yahoo.com&.tsrc=finance"
    resp = requests.get(url).json()
    closing_vals = resp["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    timestamps = resp["chart"]["result"][0]["timestamp"]
    return ({'data': closing_vals, 'Date': timestamps})

def calculate_sma(data, window_size):
    df = pd.DataFrame(data)
    #convert epoch to datetime
    df['Date'] = pd.to_datetime(df['Date'], unit='s')
    #convert to India time
    df.Date = df.Date.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
    #today mask
    todays_date = str(df.loc[df.index[-1], "Date"]).split(' ')[0]
    previous_days_date = str(df.loc[df.index[-26], "Date"]).split(' ')[0]
    mask = (df["Date"] > previous_days_date) & (df["Date"] <= todays_date)
    df['sma'] = df.rolling(window_size*int(375/DATA_STREAM_INTERVAL)).mean()
    # print(df.tail())
    # todays_stock_df = pd.DataFrame(data=df, columns=['Date', 'data'])
    return df

def SMA5(symbol):
    data_len = 30 #todays data + last 5 days data
    window_size = 5
    d = load_data(symbol, str(data_len))
    filtered_data = []
    timestamp_of_sma = None
    for idx,dd in enumerate(d['data']):
        if dd is not None:
            filtered_data.append(dd)
    #we are calculating sma for last date
    timestamp_of_sma = d['Date'][-1]

    data_sum = sum(filtered_data)
    sma = data_sum/len(filtered_data)

    print('sma_' + str(len(filtered_data)), sma, dt.datetime.fromtimestamp(int(timestamp_of_sma)))
    # return calculate_sma(d, window_size)

if __name__ == "__main__":
    # d = load_data('SBIN', day15)
    # # calculate_simple_avarages(d['dat'], window_size, d['timestamps'])
    # calculate_sma(d, 5)
    SMA5('ITC')
