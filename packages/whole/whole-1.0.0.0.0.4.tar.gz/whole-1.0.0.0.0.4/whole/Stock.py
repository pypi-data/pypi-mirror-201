#coding:utf-8
#!/usr/bin/python3
import os   #操作系统接口模块
import time #时间的访问和转换
import sqlite3  #SQLite 数据库
import sys
from whole.Run import R

PipList = os.popen("pip list").read()
#if im.find('not found') != -1:
    #os.system('sudo apt-get install -y python3-pip')    #Ubuntu安装pip
if PipList.find('baostock')==-1 :
    os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pip')#临时使用国内镜像升级pip
    os.system('pip install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple')#自动安装包
import baostock as bs#证券宝www.baostock.com

def StockData():#获取股票数据
    R(sys.argv[1],"Stock")#后台运行
    if os.name=="nt":
        sq3 = sqlite3.connect("C:\\Users\\y\\Desktop\\stock.db")#连接sqlite   Windows
    else:
        sq3 = sqlite3.connect("/root/stock.db")#连接sqlite   Linux
    c = sq3.cursor()

    bs.login() #登陆系统
    print("开始获取股票代码："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #c.execute('drop table code')    #删除表格
    c.execute("CREATE TABLE IF NOT EXISTS code (id INTEGER PRIMARY KEY,code TEXT,name TEXT,minimum TEXT)")#判断表格不存在，创建“股票代码”表格
    
    TodayDate=time.strftime("%Y-%m-%d", time.localtime())#今天日期
    rs = bs.query_trade_dates(start_date=TodayDate, end_date=TodayDate)#获取交易日
    trading_time_rs=rs.get_row_data()
    if trading_time_rs[1]=="0":#0:非交易日 1:交易日
        sys.exit(0)#退出
    trading_time = trading_time_rs[0]#股票交易时间

    stock_rs = bs.query_all_stock(trading_time)#获取股票代码
    stock_df = stock_rs.get_data()
    stock_obtain=[]
    for code,code_name in zip(stock_df["code"],stock_df["code_name"]):
        if code[0:5]=="sh.60" or code[0:5]=="sz.00":
            stock_obtain.append((code,code_name))

    c.execute("delete from code") #清空数据库表格
    sq3.commit()
    c.executemany("INSERT INTO code (code,name) VALUES (?,?)",stock_obtain)  #股票代码写入数据库
    sq3.commit()
    print("获取股票代码成功："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print("开始获取股票数据："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    stock_data_1 = []#获取股票数据列表
    c.execute("SELECT code FROM code")#选择股票表格
    stock_code_1 = c.fetchall()#获取股票表格所有记录
    #stock_code_1.extend([('sh.000001',),('sz.399001',),('sz.399006',)])
    li = len(stock_code_1)
    n = 0
    
    for stock_code_2 in stock_code_1:                                  # id                   日期       开盘价   最高价    最低价   收盘价     前收盘价         涨跌幅%     dr
        c.execute("CREATE TABLE IF NOT EXISTS ["+ stock_code_2[0] +"] (id INTEGER PRIMARY KEY,date TEXT,preclose TEXT,open TEXT,high TEXT,low TEXT,close TEXT,pctChg TEXT,dr TEXT)")   #判断表格不存在，创建股票代码表格
        n+=1
        print(stock_code_2[0]+"   总数："+str(li)+"   当前数："+str(n)+"   剩余："+str(li-n))
        c.execute("SELECT date FROM ["+ stock_code_2[0] +"] ORDER BY id DESC LIMIT 1")#最后更新日期
        lud = c.fetchone()#最后更新日期
        last_update_date = "1990-12-18" if lud==None else lud[0]#判断最后更新日期为空1990-12-18
        last_update_date_1 = time.strftime("%Y-%m-%d", time.localtime(time.mktime(time.strptime(last_update_date,'%Y-%m-%d'))+86400))  #最后更新日期加一天
        if float(time.mktime(time.strptime(last_update_date_1,"%Y-%m-%d")))<=float(time.mktime(time.strptime(trading_time,"%Y-%m-%d"))):
            #股票数据
            rs=bs.query_history_k_data_plus(stock_code_2[0],"date,preclose,open,high,low,close,pctChg",start_date=last_update_date_1, end_date="",frequency="d", adjustflag="3")
            while (rs.error_code == '0') & rs.next():
                stock_data_1.append(tuple(rs.get_row_data()))
            c.executemany("INSERT INTO ["+ stock_code_2[0] +"] (date,preclose,open,high,low,close,pctChg) VALUES (?,?,?,?,?,?,?)",stock_data_1)  #数据写入数据库
            sq3.commit()
            stock_data_1.clear()#清空列表stock_data_1
            #股票除夕除权
            last_update_years=time.strptime(last_update_date,'%Y-%m-%d').tm_year#最后更新年份
            while last_update_years <= time.localtime(time.time()).tm_year:
                rs_dividend=bs.query_dividend_data(code=stock_code_2[0],year=last_update_years,yearType="report")
                while (rs_dividend.error_code=='0') & rs_dividend.next():
                    s1 = rs_dividend.get_row_data()
                    if s1[8] != "":
                        c.execute("UPDATE ["+ stock_code_2[0] +"] SET dr=? WHERE date=?",("DR",s1[6]))
                        sq3.commit()
                last_update_years+=1
    bs.logout()#登出系统
    sq3.close
    print("获取股票数据成功："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))#获取股票数据