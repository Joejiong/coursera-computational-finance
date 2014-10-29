from math import sqrt
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import numpy as np
import datetime as dt
import csv
import sys

values_csv = sys.argv[1]
benchmark = sys.argv[2]

fund_values = []
dates = []
for row in csv.reader(open(values_csv, 'rU'), delimiter=','):
    date = dt.datetime(int(row[0]), int(row[1]), int(row[2]), hour=16)
    dates.append(date)
    value = float(row[3])
    fund_values.append(value)

start_date = dates[0]
end_date = dates[-1]
fund_daily_rets = tsu.returnize0(np.array(fund_values))

timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours=16))
dataobj = da.DataAccess('Yahoo')
benchmark_prices = dataobj.get_data(timestamps, [benchmark], 'close')
benchmark_daily_rets = tsu.returnize0(benchmark_prices.values.copy())

print 'Details of the Performance of the portfolio :'
print 'Data Range : %s to %s\n' % (str(start_date), str(end_date))

print 'Sharpe Ratio of Fund : %f' % (sqrt(252) * fund_daily_rets.mean() / fund_daily_rets.std())
print 'Sharpe Ratio of %s : %f' % (benchmark, (sqrt(252) * benchmark_daily_rets.mean() / benchmark_daily_rets.std()))
print 'Total Return of Fund : %f' % (fund_values[-1]/fund_values[0])
print 'Total Return of %s : %f' % (benchmark, benchmark_prices.values[-1]/benchmark_prices.values[0])
print 'Standard Deviation of Fund : %f' % fund_daily_rets.std()
print 'Standard Deviation of %s : %f' % (benchmark, benchmark_daily_rets.std())
print 'Average Daily Return of Fund : %f' % fund_daily_rets.mean()
print 'Average Daily Return of %s : %f' % (benchmark, benchmark_daily_rets.mean())