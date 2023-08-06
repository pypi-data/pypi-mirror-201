#coding:utf-8
#!/usr/bin/python3
import sys
import socket
import threading    #多线程_内置库
from whole.Run import R

class TCP (threading.Thread):   #线程处理函数
    def __init__(self,name):
        threading.Thread.__init__(self) #线程类必须的初始化
        self.name = name    #线程名称
    def run(self):
        print ("开始线程：" + self.name)
        i = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建socket对象 TCP
        s.bind(("0.0.0.0", 8888))  #绑定端口号
        s.listen(5)  # 设置最大连接数，超过后排队
        while True:  # 建立客户端连接
            conn, addr = s.accept()#accept默认会引起阻塞
            try:
                while True:
                    i += 1
                    msg = conn.recv(1024)  # 接收来自客户端的数据，小于1024字节
                    if len(msg) == 0:
                        break
                    print("客户端ip:"+str(addr)+"---接收内容:"+msg.decode('utf-8'))
                    conn.send(("TCP 本机IP:"+str(addr)+"---"+str(i)).encode('utf-8'))  #发送数据给客户端
                conn.close()#关闭新创建的conn
            except:
                print("异常断开连接")

class UDP (threading.Thread):   #线程处理函数
    def __init__(self,name):
        threading.Thread.__init__(self) #线程类必须的初始化
        self.name = name    #线程名称
    def run(self):
        print ("开始线程：" + self.name)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#创建socket对象 UDP
        s.bind(("0.0.0.0", 8888))
        i = 0
        while True:
            i += 1
            data,addr = s.recvfrom(1024)
            print("客户端ip:"+str(addr)+"---接收内容:"+str(data.decode('utf-8')))
            s.sendto(("UDP 本机IP:"+str(addr)+"---"+str(i)).encode('utf-8'), addr)#发送

def TU():
    R(sys.argv[1],"TCP_UDP")    #后台运行
    threads = []    #存放线程的数组，相当于线程池

    t = TCP("TCP")  #执行函数为TCP（创建线程）
    threads.append(t)   #先讲这个线程放到线程threads

    u = UDP("UDP")  #执行函数为UDP（创建线程）
    threads.append(u)   #先讲这个线程放到线程threads

    for i in threads:
        i.start()   #开启线程

    for i in threads:
        i.join()    #等待所有线程运行完毕才执行一下的代码