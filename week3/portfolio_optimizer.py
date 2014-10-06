import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
from math import sqrt

possible_allocations = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def simulate(start_date, end_date, symbols, allocations):
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    dataobj = da.DataAccess('Yahoo')

    # Reading the data, now data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    close = dataobj.get_data(ldt_timestamps, symbols, 'close')
    # Getting the numpy ndarray of close prices.
    na_price = close.values.copy()

    # Normalizing the prices to start at 1 and see relative returns
    normalized_price = (na_price / na_price[0, :]) * allocations
    portfolio_rets_cumulative = (normalized_price.copy()).sum(axis=1)
    daily_rets = tsu.returnize0(portfolio_rets_cumulative.copy())
    return daily_rets.std(), \
           daily_rets.mean(), \
           sqrt(252) * daily_rets.mean() / daily_rets.std(), \
           portfolio_rets_cumulative[-1]

start_date = dt.datetime(2011, 1, 1)
end_date = dt.datetime(2011, 12, 31)
symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']

# brute-force approach to optimize portfolio with respect to the highest Sharpe ratio
best = (None, None, float('-inf'), None, [])
for i in possible_allocations:
    for j in possible_allocations:
        for k in possible_allocations:
            for l in possible_allocations:
                if (i + j + k + l) != 1.0:
                    continue
                else:
                    vol, daily_ret, sharpe, cum_ret = simulate(start_date, end_date, symbols, [i, j, k, l])
                    if best[2] < sharpe:
                        best = (vol, daily_ret, sharpe, cum_ret, [i, j, k, l])
                    pass

print 'Start Date: %s' % str(start_date)
print 'End Date: %s' % str(end_date)
print 'Symbols: %s' % str(symbols)
print 'Optimal Allocations: %s' % str(best[4])
print 'Sharpe Ratio: %.5f' % best[2]
print 'Volatility (stdev of daily returns): %.5f' % best[0]
print 'Average Daily Return: %.5f' % best[1]
print 'Cumulative Return: %.5f' % best[3]