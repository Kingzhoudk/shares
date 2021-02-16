from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, YEARLY
from matplotlib.dates import MonthLocator, MONTHLY
import datetime as dt
import mplfinance as mpf
import pylab
import DataBase


class Gui(object):
    def animate(self,ival):
        if (20+ival) > len(df):
            print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
        data = df.iloc[0:(20+ival)]
        ax1.clear()
        ax2.clear()
        mpf.plot(data,ax=ax1,volume=ax2,**pkwargs)
    def draw(self):
        data_base = DataBase.SqlLiteData().GetCollectData2("603993.SH", "2015-01-01", "2021-02-14")
        pkwargs = dict(type='candle', mav=(10, 20))
        # 创建子图
        fig, axes = mpf.plot(data_base, returnfig=True, volume=True,
                             figsize=(11, 8), panel_ratios=(2, 1), title='\n\nS&P 500 ETF', **pkwargs)
        fig.subplots_adjust(bottom=0.2)
        # mav[movingaverage3,6,9]

        mpf.plot(data_base, ax=ax1, type='candle', mav=(3, 6, 9), volume=True)


Gui().draw()
