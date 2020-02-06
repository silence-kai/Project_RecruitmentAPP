import pymysql


class PositionModel:
    def __init__(self, db):
        self.db = db
        self.cur = self.db.cursor()

    # def close(self):
    #     cur.close()
    #     db.close()

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


# if __name__ == '__main__':
#     db = pymysql.connect(host="localhost",
#                          port=3306,
#                          user="root",
#                          password="kai199418",
#                          database="recruitment",
#                          charset="utf8")
#     model = PositionModel(db)
#     print(model.get_position("111@163.com", "测试", None, None))
    # model.add_position("开发工程师", '24000', "熟练使用python语言，了解开发流程", 1, 1)
    # print(model.get_hr("alizhangsan"))