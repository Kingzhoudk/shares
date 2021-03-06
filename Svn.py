import DataBase
from sklearn import svm
import numpy as np


class SvnData(object):
    def __init__(self, in_code, start_dt, end_dt):
        ans = self.collectData(in_code, start_dt, end_dt)

    def collectData(self, in_code, start_dt, end_dt):
        # 建立数据库连接，获取日线基础行情(开盘价，收盘价，最高价，最低价，成交量，成交额)
        dc = DataBase.SqlLiteData()
        done_set = dc.GetDate(in_code, start_dt, end_dt)
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
        # 将日线行情整合为训练集(其中self.train是输入集，self.target是输出集，self.test_case是end_dt那天的单条测试输入)
        self.data_train = []
        self.data_target = []
        self.data_target_onehot = []
        self.cnt_pos = 0
        self.test_case = []

        for i in range(1, len(self.close_list)):
            train = [self.open_list[i-1], self.close_list[i-1], self.high_list[i-1],
                     self.low_list[i-1], self.vol_list[i-1], self.amount_list[i-1]]
            self.data_train.append(np.array(train))

            if self.close_list[i]/self.close_list[i-1] > 1.0:
                self.data_target.append(float(1.00))
                self.data_target_onehot.append([1, 0, 0])
            else:
                self.data_target.append(float(0.00))
                self.data_target_onehot.append([0, 1, 0])
        self.cnt_pos = len([x for x in self.data_target if x == 1.00])
        self.test_case = np.array([self.open_list[-1], self.close_list[-1], self.high_list[-1],
                                   self.low_list[-1], self.vol_list[-1], self.amount_list[-1]])
        self.data_train = np.array(self.data_train)
        self.data_target = np.array(self.data_target)
        return 1

    def collectSvn(self):
        train = self.data_train
        target = self.data_target
        test_case = [self.test_case]
        model = svm.SVC()               # 建模
        model.fit(train, target)        # 训练
        ans2 = model.predict(test_case)  # 预测
        print(ans2[0])
        return ans2[0]