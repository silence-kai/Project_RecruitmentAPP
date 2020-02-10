import pymysql
from server_site.config import *


class PositionModel:
    def __init__(self, db):
        self.db = db
        self.cur = self.db.cursor()

    def get_position(self, account, position, salary, enterprise):
        if not position and not salary and not enterprise:
            sql = "select wanted_position from applicant where account='%s';" % account
            self.cur.execute(sql)
            result = self.cur.fetchone()
            position = result[0]

        sql = "select position.name,enterprise.enterprise_name,position.month_pay,position.content,hr.name from position " \
              "inner join enterprise on position.enterprise_id=enterprise.id " \
              "inner join hr on position.hr_id = hr.id where 1=1"
        if position:
            sql += " and position.name regexp '%s'" % (r'.*' + position + '.*')
        if salary:
            min_s, max_s = salary.split("-")
            sql += " and position.month_pay between %s and %s" % (min_s, max_s)
        if enterprise:
            sql += " and enterprise.enterprise_name regexp '%s'" % (r'.*' + enterprise + '.*')
        print(sql)
        self.cur.execute(sql)
        return self.cur.fetchall()

    def add_position(self, name, month_pay, content, hr_id, enterprise_id):
        sql = "insert into position (name,month_pay,content,hr_id,enterprise_id) values ('%s','%s','%s',%s,%s)" % (
            name, month_pay, content, hr_id, enterprise_id)
        try:
            print(sql)
            self.cur.execute(sql)
            self.db.commit()
            return 1
        except:
            self.db.rollback()
            return 0

    def get_hr(self, account):
        sql = "select * from hr where hr_account = '%s'" % account
        print(sql)
        self.cur.execute(sql)
        return self.cur.fetchone()


class AccountModel:
    def __init__(self, db):
        self.db = db
        self.cur = self.db.cursor()

    def user_information_judgment(self, account, passwd, mode):
        """
        判断用户信息是否正确，返回对应字符串辅以判断
        :param name: 用户名
        :param passwd: 密码
        :return: 对应判断字符串
        """
        sql_account = "select account from %s where account=%s"
        sql_passwd = "select password from %s where account=%s"
        self.cur.execute(sql_account, [mode, account])
        if not self.cur.fetchone():
            return "No_account"
        else:
            self.cur.execute(sql_passwd, [account])
            if self.cur.fetchone()[0] != passwd:
                return "Password_wrong"
            else:
                return "Allow_login"

    def verify_regist_info(self, account, password):
        new_account = "select account from applicant where account=%s"
        self.cur.execute(new_account, [account])
        if not self.cur.fetchone():
            sql = " insert into applicant (account,password) values ('%s','%s')" % (account, password)
            try:
                print(sql)
                self.cur.execute(sql)
                self.db.commit()
                return "Regist_success"
            except:
                self.db.rollback()
                return "Unknown_error"

        else:
            return "Account_exists"

# if __name__ == '__main__':
#     db = pymysql.connect(host="localhost",
#                          port=3306,
#                          user="root",
#                          password="kai199418",
#                          database="recruitment",
#                          charset="utf8")
# #     model = PositionModel(db)
# #     print(model.get_position("111@163.com", "测试", None, None))
#     # model.add_position("开发工程师", '24000', "熟练使用python语言，了解开发流程", 1, 1)
#     # print(model.get_hr("alizhangsan"))
#     model = AccountModel(db)
#     # print(model.user_information_judgment("111@163.com1","1234561"))
#     print(model.verify_regist_info("911077046@qq.com","1234561"))
#     print(model.verify_regist_info("911077046@qq.com", "1234561"))