import numpy as np
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep
import sys
import csv
from pandas import rolling_mean, rolling_std, DataFrame

orders_csv = sys.argv[1]


def compute_bollinger_bands(prices, look_back):
    bollinger_vals = DataFrame.copy(prices)
    for symbol in bollinger_vals._series:
        rolling_mean_vals = rolling_mean(prices[symbol], look_back, min_periods=look_back)
        rolling_std_vals = rolling_std(prices[symbol], look_back, min_periods=look_back)
        bollinger_vals[symbol] = (prices[symbol] - rolling_mean_vals) / rolling_std_vals
    return bollinger_vals


def find_events(bollinger_vals):
    ts_market = bollinger_vals['SPY']

    print "Finding Events"

    df_events = copy.deepcopy(bollinger_vals)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = bollinger_vals.index

    events = []
    for i in range(1, len(ldt_timestamps)):
        for symbol in bollinger_vals._series:
            # Calculating the returns for this timestamp
            bollinger_equity_today = bollinger_vals[symbol].ix[ldt_timestamps[i]]
            bollinger_equity_yesterday = bollinger_vals[symbol].ix[ldt_timestamps[i - 1]]
            bollinger_market_today = ts_market.ix[ldt_timestamps[i]]

            if bollinger_equity_today <= -2 and bollinger_equity_yesterday >= -2 and bollinger_market_today >= 1:
                if len(ldt_timestamps) - i > 5:
                    item = (ldt_timestamps[i], ldt_timestamps[i + 5], symbol)
                else:
                    item = (ldt_timestamps[i], ldt_timestamps[-1], symbol)
                events.append(item)
                df_events[symbol].ix[ldt_timestamps[i]] = 1
    return df_events, events


dt_start = dt.datetime(2008, 1, 1)
dt_end = dt.datetime(2009, 12, 31)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

dataobj = da.DataAccess('Yahoo')
symbols = dataobj.get_symbols_from_list('sp5002012')
symbols.append('SPY')

keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = dataobj.get_data(ldt_timestamps, symbols, keys)
d_data = dict(zip(keys, ldf_data))

for s_key in keys:
    d_data[s_key] = d_data[s_key].fillna(method='ffill')
    d_data[s_key] = d_data[s_key].fillna(method='bfill')
    d_data[s_key] = d_data[s_key].fillna(1.0)

bollinger_vals = compute_bollinger_bands(d_data['close'], 20)
df_events, events = find_events(bollinger_vals)
print "Creating Study"
ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                 s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                 s_market_sym='SPY')

writer = csv.writer(open(orders_csv, 'wb'), delimiter=',')
for (buy_date, sell_date, symbol) in events:
    row_buy = [buy_date.year, buy_date.month, buy_date.day, symbol, 'Buy', 100]
    row_sell = [sell_date.year, sell_date.month, sell_date.day, symbol, 'Sell', 100]
    writer.writerow(row_buy)
    writer.writerow(row_sell)
