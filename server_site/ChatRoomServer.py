from socket import *
import os
import pymysql
import json
import time
from server_site.config import *
from server_site.module import ChatRecord

ADDR = ('0.0.0.0', 8402)

db = pymysql.connect(host=mysql_host,
                     port=mysql_port,
                     user=mysql_user,
                     password=mysql_password,
                     database=mysql_database,
                     charset="utf8")
# 创建用户存储字典 {name:address}
applicant_list = {}
hr_list = {}


# 登录账户与ip映射
def p_login(account, addr, s):
    hr_list[account] = addr
    # 加载离线消息并发送
    records = init_record(account)
    result = deal_chat_record(records)
    data = json.dumps({"msg_type":"offline_msg","data":result})
    s.sendto(data.encode(), addr)
    # 发送完离线消息把离线消息转为在线消息
    ChatRecord(db).update_record(account)


def e_login(account, addr, s):
    hr_list[account] = addr
    # 登陆后自动加载离线消息并发送
    records = init_record(account)
    result = deal_chat_record(records)
    data = json.dumps({"msg_type":"offline_msg","data":result})
    s.sendto(data.encode(), addr)
    #发送完离线消息把离线消息转为在线消息
    ChatRecord(db).update_record(account)

#处理数据库提出得聊天记录，格式
def deal_chat_record(records):
    chat_record = []
    for i in records:
        item = (i[1],str(i[4]),i[1])
        chat_record.append(item)
    return chat_record

# 账户登录后立即加载聊天记录
def init_record(login_account):
    load_record = ChatRecord(db)
    records = load_record.select_record(login_account)
    return records


# 将所有求职者添加到用户存储字典中
def add_apps():
    allapp = ChatRecord(db).get_apps()
    for app in allapp:
        applicant_list[app[0]] = ''
    return applicant_list


# 将所有hr添加到用户存储字典中
def add_hrs():
    allhr = ChatRecord(db).get_hrs()
    for hr in allhr:
        hr_list[hr[0]] = ''
    return hr_list


# 求职者和hr相互发消息并保存消息记录
def do_chat(s, fromaccount, text, toaccount, send_time, addr):
    msg = "\n%s : %s : %s" % (fromaccount,str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), text)
    # 如果不在线
    if addr == "":
        # 如果toaccount是hr,就把消息放入数据库的hr表。
        if toaccount in hr_list:
            ChatRecord(db).insert_record(fromaccount, toaccount, text, 0, send_time)
        # 不在hr列表,就放入数据库的applicant表。
        else:
            ChatRecord(db).insert_record(fromaccount, toaccount, text, 0, send_time)
    # 在线
    else:
        if toaccount in hr_list:
            ChatRecord(db).insert_record(fromaccount, toaccount, text, 1, send_time)
        else:
            ChatRecord(db).insert_record(fromaccount, toaccount, text, 1, send_time)

        data = {"msg_type":"online_msg","data":msg}
        s.sendto(json.dumps(data).encode(), addr)


# 接受请求，分发任务
def do_request(s):
    while True:
        # 所有请求都在这里接受
        data, addr = s.recvfrom(1024)
        recv_msg = json.loads(data.decode())
        request = recv_msg["request_type"]
        data = recv_msg["data"]
        # 求职者登陆
        if request == "p_login":
            p_login(data["account"], addr, s)
        # HR登陆
        elif request == "e_login":
            e_login(data["account"], addr, s)
        # 求职者发消息
        elif request == "p_send_msg":
            do_chat(s, data["From"], data["send_content"], data["To"],
                    data["send_time"], hr_list[data["To"]])
        # HR发消息
        elif request == "e_send_msg":
            do_chat(s, data["From"], data["send_content"], data["To"],
                    data["send_time"], applicant_list[data["To"]])
        # 求职者退出
        elif request == "p_quit":
            applicant_list[request["account"]] = ""
        # HR退出
        elif request == "e_quit":
            hr_list[request["account"]] = ""


# 搭建网络
def main():
    # udp服务端网络
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)

    add_apps()
    add_hrs()
    print(hr_list)
    print(applicant_list)
    pid = os.fork()
    if pid < 0:
        print("Server Error...")
        return
    elif pid == 0:
        pass
    else:
        # 请求处理函数
        do_request(s)


if __name__ == '__main__':
    main()
