from tkinter import *
import tkinter.messagebox
from socket import *
import sys
import time
import re

ADDR = ('127.0.0.1', 8402)
hj_sock = socket()
hj_sock.connect(ADDR)
root = Tk()
root.title('Hello Job')


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

    def user_login(self):
        user_name = self.var_usr_name.get()
        user_pwd = self.var_usr_pwd.get()
        if not user_name:
            tkinter.messagebox.showinfo(title='Hello Job', message='账号不能为空')
        elif not user_pwd:
            tkinter.messagebox.showinfo(title='Hello Job', message='密码不能为空')
        hj_sock.send(b"p_login verification,%s,%s" % (user_name.encode(), user_pwd.encode()))
        self.check_login()

    def check_login(self):
        data = hj_sock.recv(1024).decode()
        if data == "user not exist":
            tkinter.messagebox.showinfo(title='Hello Job', message='账号不存在')
        elif data == "password error":
            tkinter.messagebox.showinfo(title='Hello Job', message='密码错误')
        elif data == "allow p_login":
            login_account =self.var_usr_name.get()
            self.window.destroy()
            global pview_tk
            pview_tk = Tk()
            PersonalView(pview_tk,login_account)
            pview_tk.mainloop()

    def user_register(self):
        PersonalRegister(self.window)

    def user_quit(self):
        self.window.destroy()
        hj_sock.close()


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
        Label(self.window, text='(请填写邮箱地址)', font=("黑体", 15)).place(x=550, y=200)
        Label(self.window, text='(密码为8-16位且大小写加数字)', font=("黑体", 15)).place(x=550, y=250)
        Label(self.window, text='输入账号:', font=("黑体", 15)).place(x=250, y=200)
        Label(self.window, text='输入密码:', font=("黑体", 15)).place(x=250, y=250)
        Label(self.window, text='确认密码:', font=("黑体", 15)).place(x=250, y=300)
        Label(self.window, text='验证码:', font=("黑体", 15)).place(x=250, y=350)
        Entry(self.window, textvariable=self.new_user, font=("黑体", 15)).place(x=350, y=200)
        Entry(self.window, textvariable=self.new_pwd, show='*', font=("黑体", 15)).place(x=350, y=250)
        Entry(self.window, textvariable=self.confirm_pwd, show='*', font=("黑体", 15)).place(x=350, y=300)
        Entry(self.window, textvariable=self.verify_code, font=("黑体", 15)).place(x=350, y=350)
        Button(self.window, text="获取验证码", command=self.check_code, font=("黑体", 15)).place(x=570, y=350)
        Button(self.window, text="确认", command=self.submit_regist, font=("黑体", 15)).place(x=350, y=450)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=450, y=450)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    def check_code(self):
        new_user = self.new_user.get()
        hj_sock.send(b"mail_register_code,%s" % (new_user.encode()))
        data = hj_sock.recv(1024).decode()
        if data == "mailaddr error":
            tkinter.messagebox.showinfo(title='Hello Job', message='邮箱地址有误')
        if data == "mailaddr ok":
            tkinter.messagebox.showinfo(title='Hello Job', message='验证码已发送')

    def submit_regist(self):
        new_user = self.new_user.get()
        new_pwd = self.new_pwd.get()
        confirm_pwd = self.confirm_pwd.get()
        verify_code = self.verify_code.get()
        if self.check_pwd(new_pwd, confirm_pwd):
            hj_sock.send(b"submit register,%s,%s" % (new_user.encode(), new_pwd.encode()))
            self.check_regist()

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

    def check_regist(self):
        data = hj_sock.recv(1024).decode()
        if data == "name exists":
            tkinter.messagebox.showinfo(title='Hello Job', message='账号已被注册')
        if data == "register success":
            tkinter.messagebox.showinfo(title='Hello Job', message='注册成功')
            self.window.destroy()
        if data == "code error":
            tkinter.messagebox.showinfo(title='Hello Job', message='验证码有误')

    def user_quit(self):
        self.window.destroy()


class PersonalView:
    def __init__(self, master,account):
        self.window = master
        self.window.title('Hello Job')
        self.width = 800
        self.height = 600
        self.window_postion()
        self.control_layout()
        self.account = account

    def control_layout(self):
        # 标签 用户名密码
        # Label(self.window, text='(请填写邮箱地址)', font=("黑体", 15)).place(x=550, y=200)
        # Label(self.window, text='(密码为8-16位且大小写加数字)', font=("黑体", 15)).place(x=550, y=250)
        # Label(self.window, text='输入账号:', font=("黑体", 15)).place(x=250, y=200)
        # Label(self.window, text='输入密码:', font=("黑体", 15)).place(x=250, y=250)
        # Label(self.window, text='确认密码:', font=("黑体", 15)).place(x=250, y=300)
        # Label(self.window, text='验证码:', font=("黑体", 15)).place(x=250, y=350)
        # Entry(self.window, textvariable=self.new_user, font=("黑体", 15)).place(x=350, y=200)
        # Entry(self.window, textvariable=self.new_pwd, show='*', font=("黑体", 15)).place(x=350, y=250)
        # Entry(self.window, textvariable=self.confirm_pwd, show='*', font=("黑体", 15)).place(x=350, y=300)
        # Entry(self.window, textvariable=self.verify_code, font=("黑体", 15)).place(x=350, y=350)
        # Button(self.window, text="获取验证码", command=self.check_code, font=("黑体", 15)).place(x=570, y=350)
        # Button(self.window, text="确认", command=self.submit_regist, font=("黑体", 15)).place(x=350, y=450)
        # Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=450, y=450)
        pass
    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)


class EnterpriselView:
    def __init__(self, master):
        self.window = master
        self.window.title('Hello Job')
        self.width = 800
        self.height = 600
        self.var_usr_name = StringVar()
        self.var_usr_pwd = StringVar()


PersonalView(root,"asd")
root.mainloop()
