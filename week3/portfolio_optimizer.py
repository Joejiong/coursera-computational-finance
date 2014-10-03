import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import matplotlib.pyplot as plt
import datetime as dt

possible_allocations = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def simulate(start_date, end_date, symbols, allocations):
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    dataobj = da.DataAccess('Yahoo', cachestalltime=0)

    # Reading the data, now data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    close = dataobj.get_data(ldt_timestamps, symbols, 'close')
    # Getting the numpy ndarray of close prices.
    na_price = close.values.copy()

    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]
    na_rets = na_normalized_price.copy()
    tsu.returnize0(na_rets)
    portfolio_rets = (na_rets*allocations).sum(axis=1)

    # Plotting the prices with x-axis=timestamps
    plt.clf()
    plt.plot(ldt_timestamps, na_normalized_price)
    plt.legend(symbols)
    plt.ylabel('Normalized Close')
    plt.xlabel('Date')
    #plt.show()
    return portfolio_rets.std(), portfolio_rets.mean(), 0.0, 1 + portfolio_rets[-1]


start_date = dt.datetime(2011, 1, 1)
end_date = dt.datetime(2011, 12, 31)
symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
allocations = [0.4, 0.4, 0.0, 0.2]
vol, daily_ret, sharpe, cum_ret = simulate(start_date, end_date, symbols, allocations)

# brute-force approach to optimize portfolio with respect to the highest Sharpe ratio
for i in possible_allocations:
    for j in possible_allocations:
        for k in possible_allocations:
            for l in possible_allocations:
                if (i + j + k + l) != 1.0:
                    continue
                else:
                    print (i, j, k, l)
                    pass

print 'Start Date: %s' % str(start_date)
print 'End Date: %s' % str(end_date)
print 'Symbols: %s' % str(symbols)
print 'Optimal Allocations: %s' % str(allocations)
print 'Sharpe Ratio: %.5f' % sharpe
print 'Volatility (stdev of daily returns): %.5f' % vol
print 'Average Daily Return: %.5f' % daily_ret
print 'Cumulative Return: %.5f' % cum_ret