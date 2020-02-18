"""
应聘者搜职位
author:李超
"""
import json
import pymysql
from decimal import Decimal
from time import sleep
from server_site.config import *
from server_site.module import PositionModel, AccountModel, ApplicantInfoModel

db = pymysql.connect(host=mysql_host,
                     port=mysql_port,
                     user=mysql_user,
                     password=mysql_password,
                     database=mysql_database,
                     charset="utf8")


def search_position(connfd, data):
    search_position = PositionModel(db)
    result = search_position.get_position(data["account"], data["position"], data["salary"], data["enterprise"])
    if not result:
        connfd.send(b'get_position_failed')
        return
    connfd.send(b'get_position_success')
    column = ("position", "enterprise", "salary", "duties", "hr", "hr_account")
    list_result = []
    for res in result:
        dict_res = {}
        for i in range(len(res)):
            if i == 2:
                salary = str(res[2])
                dict_res[column[i]] = salary
                continue
            dict_res[column[i]] = res[i]
        list_result.append(dict_res)
    data = {"request_type": "search_position", "data": list_result}
    print(data)
    data_send = json.dumps(data)
    sleep(0.1)
    connfd.send(data_send.encode())


def add_position(connfd, data):
    add_position = PositionModel(db)
    print(data["account"])
    hr_info = add_position.get_hr(data["account"])
    print(hr_info[0], hr_info[2])
    result = db.add_position(data["position"], data["salary"], data["duties"], hr_info[0], hr_info[2])
    print(result)
    if result:
        connfd.send(b'add_position_success')
    else:
        connfd.send(b'add_position_failed')


def verify_login(connfd, data, mode):
    """
    验证登录账号密码正确性，发送对应字节码
    :param connfd: 客户端
    :param data: 用户信息包
    :return: Non]
    """
    p_login = AccountModel(db)
    msg = p_login.user_information_judgment(data["account"], data["password"], mode)
    if msg == "No_account":
        connfd.send(b"user_not_exist")  # 账号不存在
    elif msg == "Password_wrong":
        connfd.send(b"password_error")  # 密码错误
    elif msg == "Allow_login":
        connfd.send(b"allow_login")  # 审核通过


def verify_regist(connfd, data):
    verify_regist = AccountModel(db)
    msg = verify_regist.verify_regist_info(data["account"], data["password"])
    if msg == "Account_exists":
        connfd.send(b"account_exists")
        # 账号已存在
    elif msg == "Regist_success":
        connfd.send(b"regist_success")

    elif msg == "Unknown_error":
        connfd.send(b"unknown_error")


def search_applicant(connfd, data):
    db_search = ApplicantInfoModel(db)
    result = db_search.search_applicant(data["wanted_position"], data["wanted_salary"])
    if not result:
        connfd.send(b'get_applicant_failed')
        return
    connfd.send(b'get_applicant_success')
    column = ("name", "account", "wanted_position", "wanted_salary", "id")
    result_list = []
    for res in result:
        dict_res = {}
        for i in range(len(res)):
            if i == 3:
                salary = str(res[3])
                dict_res[column[i]] = salary
                continue
            dict_res[column[i]] = res[i]
        result_list.append(dict_res)
    data = {"request_type": "get_applicant", "data": result_list}
    print(data)
    data_send = json.dumps(data)
    sleep(0.1)
    connfd.send(data_send.encode())


def complete_user_information(connfd, data):
    """
    完善用户信息，发送对应成败字节码
    :param connfd: 客户端
    :param db: 数据库
    :param data: 用户信息包
    :return: None
    """
    usrdb = ApplicantInfoModel(db)
    result = usrdb.update_user_information(data["account"], data["name"], data["wanted_salary"],
                                           data["wanted_position"],
                                           data["resume"])
    if result:
        connfd.send(b"submit_info_success")
        return
    else:
        connfd.send(b"submit_info_failed")
        return


def download_user_resume(connfd, data):
    """
    下载用户简历
    :param connfd: 客户端
    :param db: 数据库
    :param data: 传入数据
    :return: 没有简历 或 简历字符串
    """
    download_resume = ApplicantInfoModel(db)
    result = download_resume.resume_download(data['account'])
    if result == "no_resume":
        connfd.send(b'no_resume')
    else:
        connfd.send(result.encode())

# if __name__ == '__main__':
# data = '{"account": "123543@qq.com", "postion": "开发工程师", "duties": "负责开发工作","salary": "23000"}'#
# data = {"wanted_position":"程序员","wanted_salary":"0-5000"}
# search_applicant("1",data)
