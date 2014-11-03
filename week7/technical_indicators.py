import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import matplotlib.pyplot as plt
from pandas import rolling_mean, rolling_std, DataFrame

symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']
start_date = dt.datetime(2010, 1, 1)
end_date = dt.datetime(2010, 12, 31)
look_back = 20


def plot_bollinger_band(prices, symbol):
    plt.clf()
    rolling_mean_vals = rolling_mean(prices[symbol], look_back, min_periods=look_back)
    rolling_std_vals = rolling_std(prices[symbol], look_back, min_periods=look_back)
    lower_bond_vals = rolling_mean_vals - rolling_std_vals
    upper_bond_vals = rolling_mean_vals + rolling_std_vals
    plt.plot(prices.index, prices[symbol].values, label=symbol)
    plt.plot(prices.index, rolling_mean_vals)
    plt.plot(prices.index, lower_bond_vals)
    plt.plot(prices.index, upper_bond_vals)
    plt.legend([symbol, 'Moving Avg.', 'Lower Bond', 'Upper Bond'])
    plt.ylabel('Adjusted Close')
    plt.savefig("movingavg-ex.png", format='png')


def compute_bollinger_bands(prices):
    bollinger_vals = DataFrame.copy(prices)
    for symbol in symbols:
        rolling_mean_vals = rolling_mean(prices[symbol], look_back, min_periods=look_back)
        rolling_std_vals = rolling_std(prices[symbol], look_back, min_periods=look_back)
        bollinger_vals[symbol] = (prices[symbol] - rolling_mean_vals) / rolling_std_vals
    return bollinger_vals


timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours=16))
dataobj = da.DataAccess('Yahoo')
stock_prices = dataobj.get_data(timestamps, symbols, 'close')
bollinger_vals = compute_bollinger_bands(stock_prices)





