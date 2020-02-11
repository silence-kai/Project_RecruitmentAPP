from socket import *
from threading import Thread
import sys
import json
import pymysql
import time
import os

# 全局变量
HOST = '0.0.0.0'
PORT = 8401
ADDR = (HOST, PORT)
# mysql

db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     password="kai199418",
                     database="recruitment",
                     charset="utf8")


# 有特定意义的变量，或者很多函数/类中都会频繁使用的变量
# 创建用户存储字典 {name:address}
user = {}


# 用户登录

# 聊

def record_ip():
    pass
# 退出
def do_quit(s, name):
     pass


# 接受请求，分发任务
def do_request(s):
    while True:
        # 所有请求都在这里接受
        data, addr = s.recvfrom(1024*1024)
        rec_data = json.loads(data.decode()) # 拆分请求
        print(rec_data)
        # 任务分发 (LOGIN CHAT QUIT)
        if rec_data['request_type'] == "login_chat":
            record_ip()
        elif rec_data['request_type'] == "p_send_msg":
            pass
        elif rec_data['request_type'] == "e_send_msg":
            pass
        elif rec_data['request_type'] == "quit":
            if rec_data['data'] in user:
                do_quit(s, rec_data['request_type'])


# 搭建网络
def main():
    # udp服务端网络
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        # 发送管理员消息
        while True:
            text = input("管理员消息:")
            msg = "CHAT 管理员 " + text
            s.sendto(msg.encode(),ADDR)
    else:
        # 请求处理函数
        do_request(s)


if __name__ == '__main__':
    main()

