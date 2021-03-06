import csv
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import sys

orders_csv = sys.argv[1]

def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    events = []
    for i in range(1, len(ldt_timestamps)):
        for s_sym in ls_symbols:
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            # Event is found if the symbol is down more then 3% while the
            # market is up more then 2%
            if f_symprice_yest >= 5 and f_symprice_today < 5:
                if len(ldt_timestamps) - i > 5:
                    item = (ldt_timestamps[i], ldt_timestamps[i+5], s_sym)
                else:
                    item = (ldt_timestamps[i], ldt_timestamps[-1], s_sym)

                events.append(item)

    return events


dt_start = dt.datetime(2008, 1, 1)
dt_end = dt.datetime(2009, 12, 31)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

dataobj = da.DataAccess('Yahoo')
ls_symbols = dataobj.get_symbols_from_list('sp5002012')
ls_symbols.append('SPY')

ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))

for s_key in ls_keys:
    d_data[s_key] = d_data[s_key].fillna(method='ffill')
    d_data[s_key] = d_data[s_key].fillna(method='bfill')
    d_data[s_key] = d_data[s_key].fillna(1.0)

events = find_events(ls_symbols, d_data)

writer = csv.writer(open(orders_csv, 'wb'), delimiter=',')
for (buy_date, sell_date, symbol) in events:
    row_buy = [buy_date.year, buy_date.month, buy_date.day, symbol, 'Buy', 100]
    row_sell = [sell_date.year, sell_date.month, sell_date.day, symbol, 'Sell', 100]
    writer.writerow(row_buy)
    writer.writerow(row_sell)


