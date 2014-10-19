import csv
import sys
import datetime as dt
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import copy
from pandas import DataFrame, Series

starting_cash = float(sys.argv[1])
orders_csv = sys.argv[2]
values_csv = sys.argv[3]
dates = []
symbols = set()

for row in csv.reader(open(orders_csv, 'rU'), delimiter=','):
    date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
    dates.append(date)
    symbols.add(row[3])

start_date = dates[0]
end_date = dates[-1] + dt.timedelta(days=1)
timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours=16))
dataobj = da.DataAccess('Yahoo')
df_prices = dataobj.get_data(timestamps, symbols, 'close')

trade_matrix = copy.deepcopy(df_prices)
trade_matrix = trade_matrix * 0

ts_cash = Series(len(timestamps)*0, index=timestamps)
ts_cash[0] = starting_cash
trade_matrix['_CASH'] = ts_cash
for row in csv.reader(open(orders_csv, 'rU'), delimiter=','):
    date = dt.datetime(int(row[0]), int(row[1]), int(row[2]), hour=16)
    symbol = row[3]
    operation = row[4]
    amount = float(row[5])
    if operation == 'Buy':
       trade_matrix[symbol].ix[date] += amount
       trade_matrix['_CASH'].ix[date] -= amount * df_prices[symbol].ix[date]
    else:
       trade_matrix[symbol].ix[date] -= amount
       trade_matrix['_CASH'].ix[date] += amount * df_prices[symbol].ix[date]
df_holdings = copy.deepcopy(trade_matrix.cumsum())
df_prices['_CASH'] = 1.0

ts_fund_value = DataFrame(df_prices*df_holdings).sum(axis=1)
df_holdings['_VALUE'] = ts_fund_value

writer = csv.writer(open(values_csv, 'wb'), delimiter=',')
for i in ts_fund_value.index:
    row = [str(i.year), str(i.month), str(i.day), str(ts_fund_value[i])]
    writer.writerow(row)



