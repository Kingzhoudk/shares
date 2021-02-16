
from matplotlib import pyplot as plt
import mplfinance as mpf
from matplotlib.pylab import date2num
import pandas as pd
import datetime
import time
import DataBase

class DrawK:

    def Kasa(self):
        data_base = DataBase.SqlLiteData().GetCollectData2("603993.SH","2015-01-01","2021-02-14")
        # print(data_base)
        # 创建子图
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)
        # 设置X轴刻度为日期时间
        ax.xaxis_date()
        plt.xticks(rotation=45)
        plt.yticks()
        plt.title("601558")
        plt.xlabel("time")
        plt.ylabel("$")
        mpf.plot(data_base, type='candle', mav=(2, 5, 10), volume=True)

        plt.grid(True)

DrawK().Kasa()
time.sleep(100000)
    