import pymysql
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     password="kai199418",
                     database="recruitment",
                     charset="utf8")

cur = db.cursor()

# name = input("Name:")
# sql="select name,hobby,price " \
#     "from interest " \
#     "where name='%s';"%name

# sql="select name,hobby,price " \
#     "from interest " \
#     "where name=%s;"


sql = " select * from applicant where name = %s;"%(pymysql.escape_string())

cur.execute(sql) #通过参数列表给sql语句传入值

a = cur.fetchall()
print(a[0])


# 关闭游标和数据库连接
cur.close()
db.close()