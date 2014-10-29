import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import matplotlib.pyplot as plt
from pandas import rolling_mean, rolling_std

symbol = 'MSFT'
start_date = dt.datetime(2010, 1, 1)
end_date = dt.datetime(2010, 12, 31)
look_back = 20


def compute_bollinger_bands(prices):
    prices['ROLLING_MEAN'] = rolling_mean(prices[symbol], look_back, min_periods=look_back)
    prices['ROLLING_STD'] = rolling_std(prices[symbol], look_back, min_periods=look_back)
    prices['UPPER_BOND'] = prices['ROLLING_MEAN'] + prices['ROLLING_STD']
    prices['LOWER_BOND'] = prices['ROLLING_MEAN'] - prices['ROLLING_STD']
    prices['BOLLINGER_VAL'] = (prices[symbol] - prices['ROLLING_MEAN']) / prices['ROLLING_STD']
    return prices

timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours=16))
dataobj = da.DataAccess('Yahoo')
stock_prices = dataobj.get_data(timestamps, [symbol], 'close')
prices = compute_bollinger_bands(stock_prices)
plt.clf()
plt.plot(prices.index, prices[symbol].values, label=symbol)
plt.plot(prices.index, prices['ROLLING_MEAN'].values)
plt.plot(prices.index, prices['UPPER_BOND'].values)
plt.plot(prices.index, prices['LOWER_BOND'].values)
plt.legend([symbol, 'Moving Avg.', 'Upper Bond', 'Lower Bond'])
plt.ylabel('Adjusted Close')
plt.savefig("movingavg-ex.png", format='png')

print prices['BOLLINGER_VAL'].ix[dt.datetime(2010, 5, 12, 16)]




