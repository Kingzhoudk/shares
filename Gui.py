from pandas import DataFrame, Series
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, YEARLY
from matplotlib.dates import MonthLocator, MONTHLY
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# 快捷键需要的库
from matplotlib.backend_bases import key_press_handler

import tkinter
import datetime as dt
import mplfinance as mpf
import pylab
import time
import datetime

import DataBase

matplotlib.rcParams['font.sans-serif'] = ['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False     # 正常显示负号


class GuiMain(object):
    def __init__(self):
        matplotlib.use('TkAgg')
        self.table_name = "603993.SH"
        self.start_time = "2010-01-01"
        time_temp = datetime.datetime.now()
        self.end_time = time_temp.strftime('%Y%m%d')  # end_time为当天

        self.window = tkinter.Tk()
        self.window.title("Shares")     # 设置tkinter界面名字
        self.scn_w, self.scn_h = self.window.maxsize()  # 获取屏幕宽度和高度
        cen_x = (self.scn_w - 300) / 2
        cen_y = (self.scn_h - 300) / 2
        size_xy = '%dx%d+%d+%d' % (self.scn_w, self.scn_h, cen_x, cen_y)  # 设置窗口初始大小和位置
        self.window.geometry(size_xy)  # 设置窗口坐标
        # self.window.wm_attributes('-topmost', 1)  # 窗口置顶

        label_plot = tkinter.Label(self.window, text="功能区", font=("微软雅黑", 12), fg="blue")
        label_plot.place(relx=0.125, rely=0)
        label_func = tkinter.Label(self.window, text="K线图", font=("微软雅黑", 12), fg="blue")
        label_func.place(relx=0.75, rely=0)

        # 控件区
        frame1 = tkinter.Frame(self.window, bg="#808080")
        frame1.place(relx=0.00, rely=0.05, relwidth=0.25, relheight=0.95)
        self.Widget(frame1)

        # 绘图区，创建一个容器, 画K线
        self.frame2 = tkinter.Frame(self.window, bg="#c0c0c0")
        self.frame2.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.95)
        self.FigureDrawDaily(self.frame2)

    def ButtonInput(self):
        if self.input_shares_id.get()!="":
            self.table_name = self.input_shares_id.get()
        if self.input_start_time.get()!="":
            self.start_time = self.input_start_time.get()
        if self.input_end_time.get()!="":
            self.end_time = self.input_end_time.get()
        print(self.table_name)
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.FigureDrawDaily(self.frame2)
        # data_base = DataBase.SqlLiteData().GetCollectData2(
        #     self.table_name, self.start_time, self.end_time)
        # print("ButtonInput:"+data_base)
        # mpf.plot(data_base,ax=self.mpf_ax1,volume=self.mpf_ax2,**self.mpf_pkwargs)

    def ExitShares(self):
        self.window.quit()
        self.window.destroy()
        exit()

    def Widget(self,root):
        """
            负责程序控件的创建与布局
        """
        # 标签控件
        tkinter.Label(root, text='股票代码:').place(x=10, y=30)
        tkinter.Label(root, text='开始日期:').place(x=10, y=110)
        tkinter.Label(root, text='结束日期:').place(x=10, y=190)
        tkinter.Label(root, text='Svn模型预测:').place(x=10, y=390)
        tkinter.Label(root, text='其它模型预测:').place(x=10, y=430)
        # 输入框
        self.input_shares_id = tkinter.StringVar()
        entry_usr_name = tkinter.Entry(
            root, textvariable=self.input_shares_id)
        entry_usr_name.place(x=10, y=70)
        self.input_start_time = tkinter.StringVar()
        entry_usr_name = tkinter.Entry(
            root, textvariable=self.input_start_time)
        entry_usr_name.place(x=10, y=150)
        self.input_end_time = tkinter.StringVar()
        entry_usr_name = tkinter.Entry(
            root, textvariable=self.input_end_time)
        entry_usr_name.place(x=10, y=230)
        # 按纽
        bt_login = tkinter.Button(root, text='确定', command=self.ButtonInput)
        bt_login.place(x=10, y=270)
        bt_login = tkinter.Button(root, text='退出', command=self.ExitShares)
        bt_login.place(x=90, y=270)
    
    def Figure(self,root):
        """
            该函数实现的是内嵌画布,不负责画图,返回画布对象。
            :param root:父亲控件对象, 一般是容器控件或者窗体
        """
        # 画布的大小和分别率
        fig = Figure(dpi=100)
        axs = fig.add_subplot(111)
        # 创建画布
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        # 显示画布
        canvas.get_tk_widget().pack()
        # 创建工具条
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        # 显示工具条
        canvas.get_tk_widget().pack()
        # 调用快捷键
        def on_key_press(event):
            key_press_handler(event, canvas, toolbar)
        canvas.mpl_connect("key_press_event", on_key_press)
        # 返回画布的对象
        return axs

    def FigureDrawDaily(self, root):
        """
            该函数实现的是画布对象,使用mpf
            :param root:父亲控件对象, 一般是容器控件或者窗体
        """
        data_base = DataBase.SqlLiteData().GetCollectData2(
            self.table_name, self.start_time, self.end_time)
        # mav[movingaverage3,6,9]
        self.mpf_pkwargs = dict(type='candle', mav=(3, 6, 9))
        fig, axes = mpf.plot(data_base, returnfig=True, volume=True,
                             figsize=(11, 8), panel_ratios=(3, 1), title=self.table_name, **self.mpf_pkwargs)
        self.mpf_ax1 = axes[0]
        self.mpf_ax2 = axes[2]
        # 将空画布设置在tkinter上
        draw_set = FigureCanvasTkAgg(fig, root)
        # 创建工具条控件
        toolbar = NavigationToolbar2Tk(draw_set, root)
        toolbar.place(relx=0.0, rely=0.0)
        toolbar.update()
        # 显示工具条控件
        draw_set.get_tk_widget().pack(side='top', fill='both', expand=1)
    
    def update(self):
        #test
        print("test")

    def maim(self):
        self.window.mainloop()


GuiMain().maim()
