import sqlite3
import tushare as ts
import datetime
import time
import numpy as np

DataBaseSrc = "./Db/shares_cn"
DataToken = "8377af7ab3e04fd812512dbee763a394db711c3432f961d627a031a2"

def GetConn():
    conn = sqlite3.connect(DataBaseSrc)
    return conn

def GetDateTime(table_name):
    start_dt = '20100101'
    conn=GetConn()
    try:
        sql = "select * from 'main'.'%s'" % (table_name)
        cur = conn.execute(sql)
        table_data = cur.fetchall()
        if len(table_data) > 0:
            start_dt = table_data[len(table_data)-1][0]
            ans_time_stamp = time.strptime(start_dt, "%Y-%m-%d")
            start_dt = str(ans_time_stamp.tm_year)+str(ans_time_stamp.tm_mon)+str(ans_time_stamp.tm_mday)
    except:
        print("creat table: " + table_name)
        sql = 'CREATE TABLE "%s" ("state_dt" TEXT NOT NULL,"stock_code" TEXT NOT NULL,"open" REAL,\
	        "close"	REAL,"high"	REAL,"low"	REAL,"vol"	INTEGER,"amount" REAL,"pre_close"	REAL,"amt_change" REAL,"pct_change" REAL,\
            PRIMARY KEY("state_dt"))'%(table_name)
        cur = conn.execute(sql)
        conn.commit()
    conn.close()
    return start_dt

def SaveDateToday(table_name):
    # init
    ts.set_token(DataToken)
    pro=ts.pro_api()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = GetDateTime(table_name)
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y%m%d')
    # print("start_dt: "+start_dt+",end_dt: "+end_dt)
    conn = GetConn()
    try:
        df = pro.daily(ts_code=table_name, start_date=start_dt, end_date=end_dt)
        c_len = df.shape[0]
    except Exception as aa:
        print(aa)
        print('No DATA Code: ' + str(i))
        return -1
    for j in range(c_len):
        resu0 = list(df.iloc[c_len-1-j])
        resu = []
        for k in range(len(resu0)):
            if str(resu0[k]) == 'nan':
                resu.append(-1)
            else:
                resu.append(resu0[k])
        state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
        try:
            sql_insert = "INSERT INTO 'main'.'%s' ('state_dt', 'stock_code', 'open', 'close', 'high', 'low', 'vol', 'amount', 'pre_close', 'amt_change', 'pct_change') \
                VALUES('%s', '%s', %.2f, %.2f,%.2f,%.2f,%i,%.2f,%.2f,%.2f,%.2f)"\
                % (table_name,state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3]),float(resu[4]),float(resu[9]),float(resu[10]),float(resu[6]),float(resu[7]),float(resu[8]))
            # print(sql_insert)    
            re = conn.execute(sql_insert)
            conn.commit()
            # print("succeed")
        except Exception as err:
            print("error")
            continue

class DataCollect(object):
    def __init__(self, in_code,start_dt,end_dt):
        SaveDateToday(in_code);
        ans = self.collectDATA(in_code,start_dt,end_dt)
    def collectDATA(self,in_code,start_dt,end_dt):
        # 建立数据库连接，获取日线基础行情(开盘价，收盘价，最高价，最低价，成交量，成交额)
        conn = GetConn()
        sql_done_set = "SELECT * FROM 'main'.'%s' a where stock_code = '%s' and state_dt >= '%s' and state_dt <= '%s' order by state_dt asc" % (in_code,in_code, start_dt, end_dt)
        cursor = conn.execute(sql_done_set)
        done_set = cursor.fetchall()
        if len(done_set) == 0:
            raise Exception
        self.date_seq = []
        self.open_list = []
        self.close_list = []
        self.high_list = []
        self.low_list = []
        self.vol_list = []
        self.amount_list = []
        for i in range(len(done_set)):
            self.date_seq.append(done_set[i][0])
            self.open_list.append(float(done_set[i][2]))
            self.close_list.append(float(done_set[i][3]))
            self.high_list.append(float(done_set[i][4]))
            self.low_list.append(float(done_set[i][5]))
            self.vol_list.append(float(done_set[i][6]))
            self.amount_list.append(float(done_set[i][7]))
        cursor.close()
        conn.close()
        # 将日线行情整合为训练集(其中self.train是输入集，self.target是输出集，self.test_case是end_dt那天的单条测试输入)
        self.data_train = []
        self.data_target = []
        self.data_target_onehot = []
        self.cnt_pos = 0
        self.test_case = []

        for i in range(1,len(self.close_list)):
            train = [self.open_list[i-1],self.close_list[i-1],self.high_list[i-1],self.low_list[i-1],self.vol_list[i-1],self.amount_list[i-1]]
            self.data_train.append(np.array(train))

            if self.close_list[i]/self.close_list[i-1] > 1.0:
                self.data_target.append(float(1.00))
                self.data_target_onehot.append([1,0,0])
            else:
                self.data_target.append(float(0.00))
                self.data_target_onehot.append([0,1,0])
        self.cnt_pos =len([x for x in self.data_target if x == 1.00])
        self.test_case = np.array([self.open_list[-1],self.close_list[-1],self.high_list[-1],self.low_list[-1],self.vol_list[-1],self.amount_list[-1]])
        self.data_train = np.array(self.data_train)
        self.data_target = np.array(self.data_target)
        return 1    

SaveDateToday("300666.SZ")