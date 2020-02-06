from socket import *
from threading import Thread
import sys
import json
import pymysql
import time

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


class ChatServer(Thread):
    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd

    def run(self):
        while True:

            data = self.connfd.recv(1024 * 1024).decode()
            print("Request:", data)
            client_request = json.loads(data)
            if not data:
                return
            elif client_request["request_type"] == "p_get_record":
                if client_request["data"]["From"] == "迪丽热巴1":
                    data = {"from": "百度", "send_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            "send_content": "我是百度HR迪丽热巴1号"}
                    self.connfd.send(json.dumps(data).encode())
                if client_request["data"]["From"] == "迪丽热巴3":
                    data = {"from": "百度", "send_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            "send_content": "我是百度HR迪丽热巴2号"}
                    self.connfd.send(json.dumps(data).encode())
            elif client_request["request_type"] == "p_send_msg":
                if client_request["data"]["To"] == "迪丽热巴1":
                    data = {"from": "百度", "send_time": "2020.1.8", "send_content": "迪丽热巴1"}
                    self.connfd.send(json.dumps(data).encode())
                if client_request["data"]["To"] == "迪丽热巴3":
                    data = {"from": "百度", "send_time": "2020.1.8", "send_content": "迪丽热巴3"}
                    self.connfd.send(json.dumps(data).encode())


def main():
    # 创建监听套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)

    print('Listen the port 8041...')
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
        t = ChatServer(c)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()
