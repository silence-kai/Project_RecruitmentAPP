# 职位模块，增加职位，查找职位
import pymysql
import datetime


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
        sql = "select position.name,enterprise.enterprise_name,position.month_pay,position.content,hr.name,hr.hr_account from position " \
              "inner join enterprise on position.enterprise_id=enterprise.id " \
              "inner join hr on position.hr_id = hr.id where 1=1"
        if position:
            sql += " and position.name regexp '%s'" % (r'.*' + position + '.*')
        if salary:
            min_s, max_s = salary.split("-")
            sql += " and position.month_pay between %s and %s" % (min_s, max_s)
        if enterprise:
            sql += " and enterprise.enterprise_name regexp '%s'" % (r'.*' + enterprise + '.*')
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


# 账号模块，注册账号，登陆账号
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
        if mode == "applicant":
            self.sql_account = "select account from applicant where account=%s"
            self.sql_passwd = "select password from applicant where account=%s"
        elif mode == "hr":
            self.sql_account = "select hr_account from hr where hr_account=%s"
            self.sql_passwd = "select hr_password from hr where hr_account=%s"
        self.cur.execute(self.sql_account, [account])
        if not self.cur.fetchone():
            return "No_account"
        else:
            self.cur.execute(self.sql_passwd, [account])
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


# 求职者信息模块，查询求职者，完善信息，上传下载简历。
class ApplicantInfoModel:
    def __init__(self, db):
        self.db = db
        self.cur = self.db.cursor()
        self.FTP_path = "../FTP_store/"  # FTP文件库位置

    def close(self):
        self.cur.close()
        self.db.close()

    def write_file(self, resume, account):
        """
        文件写入操作
        :param resume: 简历数据
        :param account: 用户账号
        :return: 简历存储路径
        """
        file = open(self.FTP_path + account, "wb")
        file.write(resume.encode())
        file.close()
        return self.FTP_path + account

    def update_user_information(self, account, name, salary, position, resume):
        """
        更新用户信息，用于完善
        :param name: 用户名
        :param salary: 期望工资
        :param position: 期望岗位
        :param resume: 个人简历
        :return: True or False
        """
        if resume == "":
            resume_path = self.FTP_path + account
        else:
            resume_path = self.write_file(resume, account)
        updateInfo = "update applicant set name=%s,wanted_position=%s,wanted_salary=%s,resume_path=%s where account=%s;"
        try:
            self.cur.execute(updateInfo, [name, position, salary, resume_path, account])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def resume_download(self, account):
        """
        对简历下载的操作
        :param data: 客户端的用户简历
        :return: 用户简历字符串 或 不存在
        """
        sql = "select resume_path from applicant where account=%s;"
        self.cur.execute(sql, [account])
        resumePath = self.cur.fetchone()
        path = resumePath[0]
        if path:
            file = open(path, "rb")
            data = file.read()
            file.close()
            return data.decode()
        else:
            return "no_rusume"

    def search_applicant(self, wanted_position, wanted_salary):
        sql = "select name,account,wanted_position,wanted_salary,id from applicant where 1=1"
        if wanted_position:
            sql += " and wanted_position regexp '%s'" % (r'.*' + wanted_position + '.*')
        if wanted_salary:
            min_salary, max_salary = wanted_salary.split("-")
            sql += " and wanted_salary between '%s' and '%s'" % (min_salary, max_salary)
        self.cur.execute(sql)
        return self.cur.fetchall()


# 管理聊天记录
class ChatRecord:
    def __init__(self, db):
        self.db = db
        self.cur = self.db.cursor()

    # 将离线消息添加到消息记录表
    def insert_record(self, from_account, to_account, content, isofflinemsg, send_time):
        sql = 'insert into chat_record(from_account,to_account,' \
              'content,isofflinemsg,send_time) values(%s,%s,%s,%s,%s);'
        try:
            num = self.cur.execute(sql, [from_account, to_account, content, isofflinemsg, send_time])
            self.db.commit()
            return num
        except Exception as e:
            print(e)
            self.db.rollback()

    # 查询消息记录
    def select_record(self, login_account):
        sql = 'select content,from_account,to_account,isofflinemsg,send_time from ' \
              'chat_record where to_account = %s    and  isofflinemsg = 0; '
        try:
            self.cur.execute(sql, [login_account])
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(e)

    # 登录后修改离线消息为在线消息
    def update_record(self, to_account):
        sql = 'update chat_record set isofflinemsg=1 ' \
              'where to_account=%s and isofflinemsg=0;'
        try:
            self.cur.execute(sql, [to_account])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    # 查询所有app
    def get_apps(self):
        sql = 'select account from applicant;'
        self.cur.execute(sql)
        return self.cur.fetchall()

    # 查询所有hr
    def get_hrs(self):
        sql = 'select hr_account from hr;'
        self.cur.execute(sql)
        return self.cur.fetchall()


if __name__ == '__main__':
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         password='kai199418',
                         database='recruitment',
                         charset="utf8")
    a = ChatRecord(db)
    # a.insertchatrecord("123@qq.com","911077046@qq.com","hello world",0,"2020-02-21 19:40:04")
    result = a.select_record("911077046@qq.com")
    # print(datetime.datetime(2020, 2, 21, 19, 35, 4))
    # print(a.get_hrs())
    chat_record = []
    for i in result:
        item = (i[1],str(i[4]),i[1])
        chat_record.append(item)
    print(chat_record)
