import csv
import sys
import datetime as dt
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import copy
from pandas import DataFrame

starting_cash = sys.argv[1]
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

for row in csv.reader(open(orders_csv, 'rU'), delimiter=','):
    date = dt.datetime(int(row[0]), int(row[1]), int(row[2]), hour=16)
    symbol = row[3]
    operation = row[4]
    amount = row[5]
    if operation == 'Buy':
       trade_matrix[symbol].ix[date] += float(amount)
    else:
       trade_matrix[symbol].ix[date] -= float(amount)

df_holdings = copy.deepcopy(trade_matrix.cumsum())

# FIXME: Use dot product for value of whole portfolio :)
print DataFrame(df_prices*df_holdings)




