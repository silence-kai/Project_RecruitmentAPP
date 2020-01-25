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
import json

from server_site.mailtask import MailCode
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
    #
    # def login_verification(self):
    #     if MysqlHandle(db).fun01() == None:
    #         self.connfd.send(b"user not exits")
    #     else:
    #         self.connfd.send(b"user login OK")

    # 处理客户端请求
    def run(self):
        # 循环接受请求
        while True:
            data = self.connfd.recv(1024*1024).decode()
            print("Request:", data)
            client_request = json.loads(data)
            print(client_request)
            if not data:
                return
            #登陆确认，账号是否存在，密码石头正确,没问题就允许登陆
            elif client_request["request_type"] == "p_login_verification":
                pass
            #确认注册的邮箱地址是否正确，并发送验证码
            elif client_request["request_type"] == "mail_register_code":
                self.random_code = self.verify_code()
                print(self.random_code)
                if MailCode(client_request["data"]["mailaddr"], self.random_code).mail_task():
                    self.connfd.send(b"mailaddr ok")
                else:
                    self.connfd.send(b"mailaddr error")
            #确认验证码是否正确，确认账号是否存在，密码是否正确，都正确则将注册信息存入数据库。
            elif client_request["request_type"] == "submit_register":
                print(self.random_code)
                if self.random_code == client_request["data"]["verify_code"]:
                    print("注册成功")
                    self.connfd.send("register_success".encode())
                else:
                    self.connfd.send("code_error".encode())
            #完善信息，接收个人信息和简历
            elif client_request["request_type"] == "p_submit_info":
               print("把完善的个人信息写入数据库")

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