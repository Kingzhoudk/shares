import sqlite3
import tushare as ts
import datetime

DataBaseSrc = "./Db/shares"
DataToken = "8377af7ab3e04fd812512dbee763a394db711c3432f961d627a031a2"

# 定义该函数用来连接数据库
def get_conn():
    conn = sqlite3.connect(DataBaseSrc)
    return conn

class BankUser:
    def getPassword(self, name, psw):
        # 连接数据
        conn = get_conn()
        sql = "select * from user"
        cur = conn.execute(sql)
        for row in cur.fetchall():
            if(row[1] == name and row[2] == psw):
                return 1
        conn.close()
        return 0


class Money:
    def getBalance(self, table_name):
        sql = "select * from "+str(table_name)
        conn = get_conn()
        cur = conn.execute(sql)
        table_data = cur.fetchall()
        conn.close()
        table_balance = table_data[len(table_data)-1][1]
        # print(table_name+":"+str(table_balance))
        return table_balance

    def getAllRecord(self, table_name):
        conn = get_conn()
        sql = "select * from "+table_name
        cur = conn.execute(sql)
        table_data = cur.fetchall()
        conn.close()
        return table_data

    def getTotal(self):
        total = self.getBalance("manage_money") + self.getBalance("deposit") + self.getBalance("petty_cash") + self.getBalance("dream")
        return total

    # 参数说明：表名、收入+/支出-、备注信息
    def setBalance(self, table_name, record, remark):
        table_balance = self.getBalance(table_name)
        # print(table_balance)
        # 得到余额+新加入的存款金额
        table_balance += record
        sql = "insert into "+str(table_name)+"(balance,record,remark) values(" + \
            str(table_balance)+","+str(record)+",'"+str(remark)+"');"
        conn = get_conn()
        cur = conn.execute(sql)
        cur = conn.commit()
        conn.close()


'''
sd = Money()
balance = sd.getBalance("c_bank")
print(balance)
data = sd.getAllRecord("c_bank")
print(data)

def getUsers():
    try:
        uListStr = ""
        sqliteDB = sqlite3.connect(DATABASE)
        cur = sqliteDB.execute("select * from user")

        for row in cur.fetchall():
            uListStr += str(row[1])+'has the id'+str(row[0])
        sqliteDB.close()
        return uListStr
    except Exception as err:
        return err
uListStr = getUsers()
print(uListStr)


sd = Money()
balance = sd.getBalance("c_bank")
print(balance)
data = sd.getAllRecord("c_bank")
print(data)
#sd.setBalance("c_bank", -100, "test")
'''

