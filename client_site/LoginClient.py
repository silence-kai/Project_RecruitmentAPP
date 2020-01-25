from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from socket import *
import sys
import json
import time
import re

ADDR = ('127.0.0.1', 8402)
hj_sock = socket()
hj_sock.connect(ADDR)
root = Tk()
root.title('Hello Job')


# Home界面，企业和个人登录
class HomePage:
    def __init__(self, master):
        self.window = master
        self.window.title('Hello Job')
        self.width = 800
        self.height = 600
        self.imagefile = PhotoImage(file=r'backimg.PNG')
        self.background_img()
        self.window_postion()
        self.controls_postion()

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    def background_img(self):
        canvas = Canvas(self.window, height=1000, width=800)
        image = canvas.create_image(0, 0, anchor='nw', image=self.imagefile)
        canvas.pack(side='top')

    def controls_postion(self):
        Button(self.window, text='企业用户登录', command=self.enterprise_login, font=("黑体", 25)).place(x=320, y=200)
        Button(self.window, text='个人用户登录', command=self.personal_login, font=("黑体", 25)).place(x=320, y=270)
        Button(self.window, text="退出", command=self.quit_login, font=("黑体", 25)).place(x=370, y=340)

    def personal_login(self):
        self.window.destroy()
        global jump_login
        jump_login = Tk()
        PersonalLogin(jump_login)
        jump_login.mainloop()

    def enterprise_login(self):
        self.window.destroy()
        global jump_login
        jump_login = Tk()
        EnterpriseLogin(jump_login)
        jump_login.mainloop()

    def quit_login(self):
        self.window.destroy()
        hj_sock.close()


# 个人登录界面
class PersonalLogin:
    def __init__(self, master):
        self.window = master
        self.window.title('Hello Job')
        self.width = 800
        self.height = 600
        self.var_usr_name = StringVar()
        self.var_usr_pwd = StringVar()
        self.window_postion()
        self.controls_layout()

    def controls_layout(self):
        Label(self.window, text='账号:', font=("黑体", 15)).place(x=250, y=250)
        Label(self.window, text='密码:', font=("黑体", 15)).place(x=250, y=300)
        Entry(self.window, textvariable=self.var_usr_name, font=("黑体", 15)).place(x=330, y=250)
        Entry(self.window, textvariable=self.var_usr_pwd, show='*', font=("黑体", 15)).place(x=330, y=300)
        Button(self.window, text='登录', command=self.user_login, font=("黑体", 15)).place(x=250, y=350)
        Button(self.window, text='注册', command=self.user_register, font=("黑体", 15)).place(x=350, y=350)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=450, y=350)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    # 点击登录，检测账号密码是否为空，发送个人登录请求，数据：账号和密码
    def user_login(self):
        user_name = self.var_usr_name.get()
        user_pwd = self.var_usr_pwd.get()
        if not user_name:
            tkinter.messagebox.showinfo(title='Hello Job', message='账号不能为空')
        elif not user_pwd:
            tkinter.messagebox.showinfo(title='Hello Job', message='密码不能为空')
        data = {"request_type": "p_login_verification", "data": {"username": user_name, "password": user_pwd}}
        hj_sock.send(json.dumps(data).encode())
        self.check_login()

    # 接收服务器消息，账号是否存在，密码是否正确，无误就弹出个人操作页面。
    def check_login(self):
        data = hj_sock.recv(1024).decode()
        if data == "user_not_exist":
            tkinter.messagebox.showinfo(title='Hello Job', message='账号不存在')
        elif data == "password_error":
            tkinter.messagebox.showinfo(title='Hello Job', message='密码错误')
        elif data == "allow_p_login":
            login_account = self.var_usr_name.get()
            self.window.destroy()
            global pview_tk
            pview_tk = Tk()
            PersonalView(pview_tk, login_account)
            pview_tk.mainloop()

    # 弹出注册窗口
    def user_register(self):
        PersonalRegister(self.window)

    def user_quit(self):
        self.window.destroy()
        hj_sock.close()


# 企业登录界面
class EnterpriseLogin:
    def __init__(self, master):
        self.window = master
        self.window.title('Hello Job')
        self.width = 800
        self.height = 600
        self.var_usr_name = StringVar()
        self.var_usr_pwd = StringVar()
        self.window_postion()
        self.controls_layout()

    def controls_layout(self):
        Label(self.window, text='账号:', font=("黑体", 15)).place(x=250, y=250)
        Label(self.window, text='密码:', font=("黑体", 15)).place(x=250, y=300)
        Entry(self.window, textvariable=self.var_usr_name, font=("黑体", 15)).place(x=330, y=250)
        Entry(self.window, textvariable=self.var_usr_pwd, show='*', font=("黑体", 15)).place(x=330, y=300)
        Button(self.window, text='登录', command=self.user_login, font=("黑体", 15)).place(x=250, y=350)
        Button(self.window, text='注册', command=self.user_register, font=("黑体", 15)).place(x=350, y=350)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=450, y=350)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    def user_login(self):
        user_name = self.var_usr_name.get()
        user_pwd = self.var_usr_pwd.get()
        if not user_name:
            tkinter.messagebox.showinfo(title='Hello Job', message='账号不能为空')
        elif not user_pwd:
            tkinter.messagebox.showinfo(title='Hello Job', message='密码不能为空')
        hj_sock.send(b"e_login verification,%s,%s" % (user_name.encode(), user_pwd.encode()))

    def check_login(self):
        data = hj_sock.recv(128).decode()
        if data == "user not exist":
            tkinter.messagebox.showinfo(title='Hello Job', message='账号不存在')
        elif data == "password error":
            tkinter.messagebox.showinfo(title='Hello Job', message='密码错误')
        elif data == "allow e_login":
            self.window.destroy()
            global eview_tk
            eview_tk = Tk()
            EnterpriselView(eview_tk)
            eview_tk.mainloop()

    def user_register(self):
        PersonalRegister(self.window)

    def user_quit(self):
        self.window.destroy()
        hj_sock.close()


# 个人注册界面
class PersonalRegister:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title('Register Account')
        self.width = 1000
        self.height = 600
        self.new_user = StringVar()
        self.new_pwd = StringVar()
        self.confirm_pwd = StringVar()
        self.verify_code = StringVar()
        self.control_layout()
        self.window_postion()

    def control_layout(self):
        # 标签 用户名密码
        Label(self.window, text='(请填写邮箱地址)', font=("黑体", 15)).place(x=570, y=200)
        Label(self.window, text='(密码为8-16位且大小写加数字)', font=("黑体", 15)).place(x=570, y=250)
        Label(self.window, text='输入账号:', font=("黑体", 15)).place(x=250, y=200)
        Label(self.window, text='输入密码:', font=("黑体", 15)).place(x=250, y=250)
        Label(self.window, text='确认密码:', font=("黑体", 15)).place(x=250, y=300)
        Label(self.window, text='验证码:', font=("黑体", 15)).place(x=250, y=350)
        Entry(self.window, textvariable=self.new_user, font=("黑体", 15)).place(x=350, y=200)
        Entry(self.window, textvariable=self.new_pwd, show='*', font=("黑体", 15)).place(x=350, y=250)
        Entry(self.window, textvariable=self.confirm_pwd, show='*', font=("黑体", 15)).place(x=350, y=300)
        Entry(self.window, textvariable=self.verify_code, font=("黑体", 15)).place(x=350, y=350)
        Button(self.window, text="获取验证码", command=self.get_reg_code, font=("黑体", 15)).place(x=570, y=350)
        Button(self.window, text="确认", command=self.submit_regist, font=("黑体", 15)).place(x=350, y=450)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=450, y=450)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    # 验证码请求，发送注册的邮箱地址
    def get_reg_code(self):
        mailaddr = self.new_user.get()
        data = {"request_type": "mail_register_code",
                "data": {"mailaddr": mailaddr}}
        hj_sock.send(json.dumps(data).encode())
        data = hj_sock.recv(1024).decode()
        if data == "mailaddr_error":
            tkinter.messagebox.showinfo(title='Hello Job', message='邮箱地址有误')
        if data == "mailaddr_ok":
            tkinter.messagebox.showinfo(title='Hello Job', message='验证码已发送')

    # 发送提交注册请求，个人账号，密码，验证码
    def submit_regist(self):
        new_user = self.new_user.get()
        new_pwd = self.new_pwd.get()
        confirm_pwd = self.confirm_pwd.get()
        verify_code = self.verify_code.get()
        if self.check_pwd(new_pwd, confirm_pwd):
            data = {"request_type": "submit_register", "data":
                {"p_account": new_user, "password": new_pwd, "verify_code": verify_code}}
            hj_sock.send(json.dumps(data).encode())
            self.check_regist()

    # 检查密码是否为空，两次是否一致，是否合规
    def check_pwd(self, new_pwd, confirm_pwd):
        if not new_pwd or not confirm_pwd:
            tkinter.messagebox.showinfo(title='Hello Job', message='密码不能为空')
            return False
        elif new_pwd != confirm_pwd:
            tkinter.messagebox.showinfo(title='Hello Job', message='两次密码不一致')
            return False
        elif not re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[\w]{8,12}$", new_pwd):
            tkinter.messagebox.showinfo(title='Hello Job', message='密码不合规')
            return False
        else:
            return True

    # 接收服务回复，账号是否已存在，验证码是否有问题，注册成功，退出窗口
    def check_regist(self):
        data = hj_sock.recv(1024).decode()
        if data == "name_exists":
            tkinter.messagebox.showinfo(title='Hello Job', message='账号已被注册')
        if data == "register_success":
            tkinter.messagebox.showinfo(title='Hello Job', message='注册成功')
            self.window.destroy()
        if data == "code_error":
            tkinter.messagebox.showinfo(title='Hello Job', message='验证码有误')

    def user_quit(self):
        self.window.destroy()


# 个人操作界面
class PersonalView:
    def __init__(self, master, account):
        self.window = master
        self.window = Toplevel(master)
        self.window.title('Hello Job')
        self.width = 1200
        self.height = 800
        self.window_postion()
        self.control_layout()
        self.account = account
        self.test = StringVar()

    def control_layout(self):
        # 标签 用户名密码
        # Label(self.window, text='(请填写邮箱地址)', font=("黑体", 15)).place(x=550, y=200)
        # Label(self.window, text='(密码为8-16位且大小写加数字)', font=("黑体", 15)).place(x=550, y=250)
        # Label(self.window, text='输入账号:', font=("黑体", 15)).place(x=250, y=200)
        # Label(self.window, text='输入密码:', font=("黑体", 15)).place(x=250, y=250)
        # Label(self.window, text='确认密码:', font=("黑体", 15)).place(x=250, y=300)
        # Label(self.window, text='验证码:', font=("黑体", 15)).place(x=250, y=350)
        # Entry(self.window, textvariable=self.new_user, font=("黑体", 15)).place(x=350, y=200)
        # Entry(self.window, textvariable=self.new_pwd, font=("黑体", 15)).place(x=350, y=250)
        # Entry(self.window, textvariable=self.confirm_pwd, show='*', font=("黑体", 15)).place(x=350, y=300)
        # Entry(self.window, textvariable=self.verify_code, font=("黑体", 15)).place(x=350, y=350)
        Button(self.window, text="完善信息", command=self.complete_info, font=("黑体", 15)).place(x=570, y=350)
        Button(self.window, text="查询工作", command=self.find_job, font=("黑体", 15)).place(x=350, y=450)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=450, y=450)
        pass

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    def user_quit(self):
        self.window.destroy()
        hj_sock.close()

    # 查询工作，按条件，公司名，薪资，岗位
    def find_job(self):
        pass

    # 完善个人信息，登录登出时间，期望薪资，期望职位
    def complete_info(self):
        PersonalInfo(self.window,self.account)


# 提交个人信息界面
class PersonalInfo:

    def __init__(self, master,account):
        self.account = account
        self.window = Toplevel(master)
        self.window.title('Complete Personal Information')
        self.width = 600
        self.height = 400
        self.person_name = StringVar()
        self.expected_salary = StringVar()
        self.expected_postion = StringVar()
        self.control_layout()
        self.window_postion()
        self.resume_conent = None

    def control_layout(self):
        Label(self.window, text='个人姓名:', font=("黑体", 15)).place(x=150, y=80)
        Label(self.window, text='期望工资:', font=("黑体", 15)).place(x=150, y=120)
        Label(self.window, text='期望岗位:', font=("黑体", 15)).place(x=150, y=160)
        Label(self.window, text='上传简历:', font=("黑体", 15)).place(x=150, y=200)
        Entry(self.window, textvariable=self.person_name, font=("黑体", 15)).place(x=250, y=80)
        Entry(self.window, textvariable=self.expected_salary, font=("黑体", 15)).place(x=250, y=120)
        Entry(self.window, textvariable=self.expected_postion, font=("黑体", 15)).place(x=250, y=160)
        self.resume_path = Entry(self.window, width='20', font=("黑体", 15))
        self.resume_path.grid(row=0, column=1)
        self.resume_path.place(x=250, y=200)
        Button(self.window, text="选择文件", command=self.select_file, font=("黑体", 15)).place(x=460, y=200)
        Button(self.window, text="提交", command=self.submit_info, font=("黑体", 15)).place(x=250, y=280)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=350, y=280)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    # 确认提交个人信息
    def submit_info(self):
        expected_salary = self.expected_salary.get()
        expected_postion = self.expected_postion.get()
        person_name = self.person_name.get()
        print(person_name)
        print(expected_postion)
        print(expected_salary)
        print(self.resume_conent)
        data = {"request_type": "p_submit_info", "data":
            {"account":self.account,"name":person_name,"expected_salary": expected_salary, "expected_postion": expected_postion,"resume":self.resume_conent}}

        hj_sock.send(json.dumps(data).encode())

    # 确认是否提交成功
    def confirm_submit(self):
        data = hj_sock.recv(1024).decode()
        if data == "submit_info_success":
            tkinter.messagebox.showinfo(title='Hello Job', message='提交成功')
            self.window.destroy()
        if data == "submit_info_failed":
            tkinter.messagebox.showinfo(title='Hello Job', message='提交失败')

    # 选择简历文件
    def select_file(self):
        selectfile = tkinter.filedialog.askopenfilename()
        self.resume_path.insert(0, selectfile)
        self.read_resume(selectfile)

    # 读取选择文件中的内容
    def read_resume(self, file_path):
        f = open(file_path, "r",encoding="utf-8")
        self.resume_conent = f.read()

    def user_quit(self):
        self.window.destroy()


# 企业操作界面
class EnterpriselView:
    def __init__(self, master):
        self.window = master
        self.window.title('Hello Job')
        self.width = 800
        self.height = 600
        self.var_usr_name = StringVar()
        self.var_usr_pwd = StringVar()


# HomePage(root)
PersonalView(root, "asd")
# PersonalInfo(root)
root.mainloop()
