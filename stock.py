import argparse
import requests
import json
from colored import fg, bg, attr
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as md


APIKEY = "5893739aa667bc7d8916c612ece7baee" #financialmodelinggrep.com
# APIKEY = "c48f471f84227f3a7175af3785b7e365"
EXCHANGE_NAME = "NSE"
INTERVAL = 30 #in sec


class StockData:
    def __init__(self, plot_required=False):
        if plot_required:
            # %formatting x axis
            _, ax = plt.subplots(figsize=(8,6))
            ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
            plt.xlabel("Time")
            plt.ylabel("Price")

    def search(self, query):
        url = (
            "https://financialmodelingprep.com/api/v3/search?query="
            + query
            + "&limit=10&exchange="
            + EXCHANGE_NAME
            + "&apikey="
            + APIKEY
        )
        try:
            resp = requests.get(url).json()
        except Exception as e:
            print(e)
        for response in resp:
            print(response["name"], "----->", fg(1) + response["symbol"] + attr(0))

    #symbol is reffered as company short name
    def get_important_data(self, symbol):
        url = "https://financialmodelingprep.com/api/v3/quote/" + symbol +"?apikey=" + APIKEY
        try:
            resp = requests.get(url).json()[0]
        except Exception as e:
            print(e)
        # resp = requests.get(url).json()[0]
        print("---------------------------" + resp["name"] + " - " + resp["symbol"] + " " + fg(52) + bg(195) + str(resp['price']) + attr(0) + " ----------------------------------")
        print("Today Low-High: " + fg(1) + str(resp['dayLow']) + fg(34) + " - " +str(resp['dayHigh']) + attr(0))
        print("Last Closed: " + fg(207) + str(resp['previousClose']) + attr(0))
        print("Opened: " + fg(214) + str(resp['open']) + attr(0))
        print("price avg 50d/200d: " + fg(112) + str(resp['priceAvg50']) + '/' + fg(214) + str(resp['priceAvg200']) + attr(0))
        print("Year Low-High: " + fg(1) + str(resp['yearLow']) + fg(34) + " - " +str(resp['yearHigh']) + attr(0))
        print("Eps-P/E: " + fg(77) + str(resp['eps']) + ' - ' + fg(76) + str(resp['pe']) + attr(0))
        
    #todays real time time series data
    def get_time_series_data(self, symbol):
        url = "https://query1.finance.yahoo.com/v8/finance/chart/" + symbol + "?region=IN&lang=en-IN&includePrePost=false&interval=1m&range=1d&corsDomain=in.finance.yahoo.com&.tsrc=finance"
        resp = requests.get(url).json()
        timestamp = resp['chart']['result'][0]['timestamp']
        high_datas = resp['chart']['result'][0]['indicators']['quote'][0]['high']
        stock_name = resp['chart']['result'][0]['meta']['symbol']
        for indx, ts in enumerate(timestamp):
            timestamp[indx] = dt.datetime.fromtimestamp(int(ts))

        #for every get request we analyze data
        self.analyze(timestamp, high_datas)
        return[timestamp, high_datas, stock_name]


    def update_real_time_plot(self, symbol):
        for i in range(1000):
            timestamp, high_datas, stock_name = self.get_time_series_data(symbol)
            plt.title(stock_name)
            plt.plot(timestamp, high_datas)
            plt.pause(INTERVAL)
            plt.clf()
        plt.show()

#TODO
    def analyze(self, timestamp, data):
        # print("analyze data here")
        self.notify()

#Todo
    def notify(self):
        #if analysis result is good notify user
        print("notified")


if __name__ == "__main__":
    #add argparser
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', dest='query',
                    help='search a stock symbol')
    parser.add_argument('-i', dest='view',
                    help='View important stats')
    parser.add_argument('-p', dest='plot',
                    help='Plot a stock data')
    results = parser.parse_args()
    

    if results.query is not None:
        #Creating object
        stock = StockData()
        stock.search(results.query)
    elif results.view is not None:
        #Creating object
        stock = StockData()
        stock.get_important_data(results.view)
    elif results.plot is not None:
        #Creating object
        stock = StockData(plot_required=True)
        stock.update_real_time_plot(results.plot)

