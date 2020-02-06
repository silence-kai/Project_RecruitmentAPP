"""
应聘者搜职位
author:李超
"""
import json
from decimal import Decimal
from time import sleep

from server_site.module import PositionModel


def search_position(connfd, dbc, data):
    db = PositionModel(dbc)
    # print(data)
    result = db.get_position(data["account"], data["position"], data["salary"], data["enterprise"])
    if not result:
        connfd.send(b'get_position_failed')
        return
    connfd.send(b'get_position_success')
    column = ("position", "enterprise", "salary", "duties", "hr")
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
    data_send = json.dumps(data)
    sleep(0.1)
    print(data_send.encode())
    connfd.send(data_send.encode())
    # sleep(0.1)
    # connfd.send(b'##')


def add_position(connfd, dbc, data):
    db = PositionModel(dbc)
    print(data["account"])
    hr_info = db.get_hr(data["account"])
    print(hr_info[0], hr_info[2])
    result = db.add_position(data["position"], data["salary"], data["duties"], hr_info[0], hr_info[2])
    print(result)
    if result:
        connfd.send(b'add_position_success')
    else:
        connfd.send(b'add_position_failed')


# if __name__ == '__main__':
#     data = '{"account": "123543@qq.com", "postion": "开发工程师", "duties": "负责开发工作","salary": "23000"}'
