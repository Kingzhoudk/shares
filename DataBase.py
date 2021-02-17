import sqlite3
import tushare as ts
import datetime
import time
import pandas as pd
from matplotlib.pylab import date2num


class SqlLiteData(object):
    def __init__(self):
        self.data_base_src_ = "./Db/shares_cn"
        self.data_token_ = "8377af7ab3e04fd812512dbee763a394db711c3432f961d627a031a2"

    def GetConn(self):
        conn = sqlite3.connect(self.data_base_src_)
        return conn

    def GetDateTime(self, table_name):
        start_dt = '20100101'
        conn = self.GetConn()
        try:
            sql = "select * from 'main'.'%s'" % (table_name)
            cur = conn.execute(sql)
            table_data = cur.fetchall()
            if len(table_data) > 0:
                start_dt = table_data[len(table_data)-1][0]
                ans_time_stamp = time.strptime(start_dt, "%Y-%m-%d")
                start_dt = str(ans_time_stamp.tm_year) + \
                    str(ans_time_stamp.tm_mon)+str(ans_time_stamp.tm_mday)
        except:
            print("error")
        conn.close()
        return start_dt

    def CreatTable(self,table_name):
        conn = self.GetConn()
        print("creat table: " + table_name)
        sql = 'CREATE TABLE "%s" ("state_dt" TEXT NOT NULL,"stock_code" TEXT NOT NULL,"open" REAL,\
            "close"	REAL,"high"	REAL,"low"	REAL,"vol"	INTEGER,"amount" REAL,"pre_close"	REAL,"amt_change" REAL,"pct_change" REAL,\
            PRIMARY KEY("state_dt"))' % (table_name)
        cur = conn.execute(sql)
        conn.commit()
        conn.close()

    def SaveDateToday(self, table_name):
        # init
        ts.set_token(self.data_token_)
        pro = ts.pro_api()
        # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
        start_dt = self.GetDateTime(table_name)
        time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
        end_dt = time_temp.strftime('%Y%m%d')
        # print("start_dt: "+start_dt+",end_dt: "+end_dt)
        conn = self.GetConn()
        try:
            df = pro.daily(ts_code=table_name,
                           start_date=start_dt, end_date=end_dt)
            c_len = df.shape[0]
            print(c_len)
            if c_len != 0 and start_dt == "20100101":
                self.CreatTable(table_name)
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + table_name)
            return -1
        for j in range(c_len):
            resu0 = list(df.iloc[c_len-1-j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(
                resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO 'main'.'%s' ('state_dt', 'stock_code', 'open', 'close', 'high', 'low', 'vol', 'amount', 'pre_close', 'amt_change', 'pct_change') \
                    VALUES('%s', '%s', %.2f, %.2f,%.2f,%.2f,%i,%.2f,%.2f,%.2f,%.2f)"\
                    % (table_name, state_dt, str(resu[0]), float(resu[2]), float(resu[5]), float(resu[3]), float(resu[4]), float(resu[9]), float(resu[10]), float(resu[6]), float(resu[7]), float(resu[8]))
                # print(sql_insert)
                re = conn.execute(sql_insert)
                conn.commit()
                # print("succeed")
            except Exception as err:
                print("error")
                continue

    def GetDate(self, table_name, start_time, end_time):
        self.SaveDateToday(table_name)
        conn = self.GetConn()
        try:
            sql_done_set = "SELECT * FROM 'main'.'%s' a where stock_code = '%s' and state_dt >= '%s' and state_dt <= '%s' order by state_dt asc" % (
                table_name, table_name, start_time, end_time)
            cursor = conn.execute(sql_done_set)
            done_set = cursor.fetchall()
        except:
            print("GetDate failed")
        conn.close()
        return done_set

    def CollectData(self, table_name, start_time, end_time):
        done_set = self.GetDate(table_name, start_time, end_time)
        data_list = []
        for i in range(len(done_set)):
            date_time = datetime.datetime.strptime(done_set[i][0], '%Y-%m-%d')
            state_date = date2num(date_time)
            open = float(done_set[i][2])
            close = float(done_set[i][3])
            high = float(done_set[i][4])
            low = float(done_set[i][5])
            vol = int(done_set[i][6])
            amount = float(done_set[i][7])
            pre_close = float(done_set[i][8])
            amt_change = float(done_set[i][9])
            pct_change = float(done_set[i][10])
            datas = []
            datas = (state_date, open, close, high, low, vol,
                     amount, pre_close, amt_change, pct_change)
            data_list.append(datas)
        return data_list

    def GetCollectData1(self, table_name, start_time, end_time):
        done_set = self.GetDate(table_name, start_time, end_time)
        data_list = []
        for i in range(len(done_set)):
            date_time = datetime.datetime.strptime(done_set[i][0], '%Y-%m-%d')
            state_date = date2num(date_time)
            open = float(done_set[i][2])
            close = float(done_set[i][3])
            high = float(done_set[i][4])
            low = float(done_set[i][5])
            datas = (state_date, open, high, low, close)
            data_list.append(datas)
        return data_list

    def GetCollectData2(self, table_name, start_time, end_time):
        done_set = self.GetDate(table_name, start_time, end_time)
        data_list = []
        for i in range(len(done_set)):
            state_date = done_set[i][0]
            open = float(done_set[i][2])
            close = float(done_set[i][3])
            high = float(done_set[i][4])
            low = float(done_set[i][5])
            vol = int(done_set[i][6])
            datas = (state_date, open, high, low, close, vol)
            data_list.append(datas)
        returndata = pd.DataFrame(data_list, columns=[
                                  "DateTime", "Open", "High", "Close", "Low", "Volume"])
        # !!!把这一列设置为index, inplace = True替换原DataFrame
        returndata.set_index("DateTime", inplace=True)
        # !!!将索引类型更改为DatetimeIndex
        returndata.index = pd.DatetimeIndex(returndata.index)
        return returndata
