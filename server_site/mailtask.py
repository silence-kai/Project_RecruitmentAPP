#!/usr/bin/python3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# 第三方 SMTP 服务
class MailCode:
    def __init__(self,receivers,virify_code):
        self.__mail_host = "smtp.qq.com"
        self.__sender = '911077046@qq.com'
        self.__mail_pass = "uctrsytiboakbbhh"
        self.receivers = receivers
        self.virify_code = virify_code

    def mail_task(self):
        message = MIMEText(str(self.virify_code),'plain', 'utf-8')
        message['From'] = self.__sender
        message['To'] = self.receivers
        subject = 'Hello Job 验证码'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.__mail_host, 465)  # 465 为 SMTP 端口号
            smtpObj.login(self.__sender, self.__mail_pass)
            smtpObj.sendmail(self.__sender, self.receivers, message.as_string())
            print("邮件发送成功")
            return True
        except smtplib.SMTPException:
            print("Error: 邮件发送失败")
            return False