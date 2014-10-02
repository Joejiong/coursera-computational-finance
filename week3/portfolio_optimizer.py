import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import matplotlib.pyplot as plt
import datetime as dt


def simulate(start_date, end_date, symbols, allocations):
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, keys)
    data = dict(zip(keys, ldf_data))
    # Getting the numpy ndarray of close prices.
    na_price = data['close'].values

    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]
    cum_ret = na_normalized_price.sum(axis=1)

    # Plotting the prices with x-axis=timestamps
    plt.clf()
    plt.plot(ldt_timestamps, na_normalized_price)
    plt.legend(symbols)
    plt.ylabel('Normalized Close')
    plt.xlabel('Date')
    plt.show()
    return 0.0, 0.0, 0.0, cum_ret[-1]


start_date = dt.datetime(2011, 1, 1)
end_date = dt.datetime(2011, 12, 31)
symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
allocations = [0.4, 0.4, 0.0, 0.2]
vol, daily_ret, sharpe, cum_ret = simulate(start_date, end_date, symbols, allocations)

print 'Start Date: %s' % str(start_date)
print 'End Date: %s' % str(end_date)
print 'Symbols: %s' % str(symbols)
print 'Optimal Allocations: %s' % str(allocations)
print 'Sharpe Ratio: %.3f' % sharpe
print 'Volatility (stdev of daily returns): %.3f' % vol
print 'Average Daily Return: %.3f' % daily_ret
print 'Cumulative Return: %.3f' % cum_ret