"""
ftp 文件服务器，服务端
env: python3.6
多线程并发，socket
"""

from socket import *
from threading import Thread
import sys
import os
from time import sleep
from sendmail import MailCode
import random
import pymysql


# 全局变量
HOST = '0.0.0.0'
PORT = 8402
ADDR = (HOST, PORT)
# mysql
# db = pymysql.connect(host="localhost",
#                      port=3306,
#                      user="root",
#                      password="kai199418",
#                      database="school",
#                      charset="utf8")

# 文件处理功能
class HelloJobServer(Thread):
    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd
        self.random_code = ""

    def verify_code(self):
        str_code = ""
        for i in range(6):
            str_code += str(random.randint(0, 9))
        return str_code

    # 处理客户端请求
    def run(self):
        # 循环接受请求
        while True:
            data = self.connfd.recv(1024).decode()
            print("Request:", data)
            client_request = data.split(",")
            print(client_request)
            if not data:
                return
            if client_request[0] == "login verification":
                pass
            if client_request[0] == "mail_register_code":
                self.random_code = self.verify_code()
                print(self.random_code)
                if MailCode(client_request[1], self.random_code).mail_task():
                    self.connfd.send(b"mailaddr ok")
                else:
                    self.connfd.send(b"mailaddr error")
            if client_request[0] == "submit register":
                print(self.random_code)
                if self.random_code == client_request[3]:
                    print("注册成功")
                    # Mysql储存client_request账号(邮箱地址)  孙国建
                    self.connfd.send("register success".encode())
                else:
                    self.connfd.send("code error".encode())

class HelloJob:
    pass

# 网络功能
def main():
    # 创建监听套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)

    print('Listen the port 8042...')
    # 循环等待客户端连接
    while True:
        try:
            c, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        # 客户端连接 ，创建线程
        t = HelloJobServer(c)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()