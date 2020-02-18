from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from socket import *
import json
import time
import re
from threading import Thread

ADDR = ('127.0.0.1', 8402)
hj_sock = socket()
hj_sock.connect(ADDR)
root = Tk()
root.title('Hello Job')


# Home界面，企业和个人登录
class HomePage():
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
        else:
            data = {"request_type": "p_login_verification", "data": {"account": user_name, "password": user_pwd}}
            hj_sock.send(json.dumps(data).encode())
            self.check_login()

    # 接收服务器消息，账号是否存在，密码是否正确，无误就弹出个人操作页面。
    def check_login(self):
        data = hj_sock.recv(1024).decode()
        if data == "user_not_exist":
            tkinter.messagebox.showinfo(title='Hello Job', message='账号不存在')
        elif data == "password_error":
            tkinter.messagebox.showinfo(title='Hello Job', message='密码错误')
        elif data == "allow_login":
            login_account = self.var_usr_name.get()
            self.window.destroy()
            global pview_tk
            pview_tk = Tk()
            client = PersonalView(pview_tk, login_account)
            client.start()
            pview_tk.mainloop()

    # 弹出注册窗口
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
        Entry(self.window, textvariable=self.new_pwd, font=("黑体", 15)).place(x=350, y=250)
        Entry(self.window, textvariable=self.confirm_pwd, font=("黑体", 15)).place(x=350, y=300)
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
                {"account": new_user, "password": new_pwd, "verify_code": verify_code}}
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
        if data == "regist_success":
            tkinter.messagebox.showinfo(title='Hello Job', message='注册成功')
            self.window.destroy()
        elif data == "account_exists":
            tkinter.messagebox.showinfo(title='Hello Job', message='账号已被注册')
        elif data == "code_error":
            tkinter.messagebox.showinfo(title='Hello Job', message='验证码有误')
        elif data == "unknown_error":
            tkinter.messagebox.showinfo(title='Hello Job', message='未知错误')

    def user_quit(self):
        self.window.destroy()


# 个人操作界面
class PersonalView(Thread):
    ADDR = ('127.0.0.1', 8401)
    chat_sock = socket(AF_INET, SOCK_DGRAM)

    def __init__(self, master, account):
        super().__init__()
        self.window = master
        self.window.title('Hello Job')
        self.width = 1200
        self.height = 800
        self.company_name = StringVar()
        self.postion_name = StringVar()
        self.window_postion()
        self.control_layout()
        self.account = account
        self.chat_info = ""
        self.choose_hr = ""
        self.hr_dict={}

    def control_layout(self):
        Label(self.window, text='找工作，就来Hello Job!!!', font=("黑体", 25)).place(x=50, y=50)
        Label(self.window, text='公司名称:', font=("黑体", 15)).place(x=50, y=150)
        Label(self.window, text='职位名称:', font=("黑体", 15)).place(x=220, y=150)
        Label(self.window, text='薪资范围:', font=("黑体", 15)).place(x=390, y=150)
        Label(self.window, text='温馨提示：双击表中的HR，可以直接与HR沟通哦！', font=("黑体", 15)).place(x=100, y=450)
        self.tip_chat = Label(self.window, text='', font=("黑体", 15)).place(x=700, y=120)
        Entry(self.window, textvariable=self.company_name, width=15, font=("黑体", 15)).place(x=50, y=180)
        Entry(self.window, textvariable=self.postion_name, width=15, font=("黑体", 15)).place(x=220, y=180)
        self.salary_range = ttk.Combobox(self.window, width=15, font=("黑体", 15))
        self.salary_range.pack()
        self.salary_range.place(x=390, y=180)
        self.salary_range['value'] = ('0 - 5000', '5000 - 10000', '10000 - 20000', '20000以上')
        Button(self.window, text="完善个人信息", command=self.complete_info, font=("黑体", 15)).place(x=900, y=50)
        Button(self.window, text="查询", command=self.search_job, font=("黑体", 15)).place(x=600, y=160)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=1050, y=50)
        self.frame = Frame(self.window)
        self.frame.place(x=50, y=240, width=650, height=200)
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.title = ['1', '2', '3', '4', '5', ]
        self.data_tree = ttk.Treeview(self.frame, columns=self.title,
                                      yscrollcommand=self.scrollbar.set,
                                      show='headings')
        self.data_tree.column('1', width=100)
        self.data_tree.column('2', width=150)
        self.data_tree.column('3', width=100)
        self.data_tree.column('4', width=150)
        self.data_tree.column('5', width=100)
        self.data_tree.heading('1', text='职位')
        self.data_tree.heading('2', text='公司')
        self.data_tree.heading('3', text='薪水')
        self.data_tree.heading('4', text='工作内容')
        self.data_tree.heading('5', text="联系HR")
        self.scrollbar.config(command=self.data_tree.yview)
        self.data_tree.pack(side=LEFT, fill=Y)
        self.data_tree.bind('<Double-1>', self.treeviewClick)
        self.text_msglist = Text(self.window, width=65, height=23, bg='white')
        self.text_msglist.place(x=700, y=150)
        self.text_msglist.tag_config("green", foreground='green')
        self.text_msg = Text(self.window, width=65, height=10, bg='white')
        self.text_msg.place(x=700, y=460)
        self.send_msg = Button(self.window, text="发送", command=self.send_chatmsg, font=("黑体", 15)).place(x=700, y=600)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    # 完善个人信息，登录登出时间，期望薪资，期望职位
    def complete_info(self):
        PersonalInfo(self.window, self.account)

    # 查询工作，按条件，公司名，薪资，岗位
    def search_job(self):
        company_name = self.company_name.get()
        postion_name = self.postion_name.get()
        salary_range = self.salary_range.get()
        if salary_range == "20000以上":
            data = {"request_type": "search_position", "data":
                {"account": self.account, "position": postion_name, "salary": "20000-999999", "enterprise": company_name
                 }}
            hj_sock.send(json.dumps(data).encode())
        else:
            data = {"request_type": "search_position", "data":
                {"account": self.account, "position": postion_name, "salary": salary_range, "enterprise": company_name
                 }}
            hj_sock.send(json.dumps(data).encode())
        rec_data = hj_sock.recv(1024 * 1024).decode()
        if rec_data == "get_position_failed":
            tkinter.messagebox.showinfo(title='Hello Job', message='没有找到符合的工作')
        elif rec_data == "get_position_success":
            self.clear_jobdata()
            self.insert_jobdata()

    # 在查询工作前先清空之前查询的结果
    def clear_jobdata(self):
        x = self.data_tree.get_children()
        for item in x:
            self.data_tree.delete(item)

    # 将返回的结果写入列表
    def insert_jobdata(self):
        rec_data = hj_sock.recv(1024 * 1024).decode()
        result = json.loads(rec_data)
        self.hr_dict.clear()
        for i in result["data"]:
            list = (i['position'], i['enterprise'], i['salary'], i['duties'], i['hr'])
            self.hr_dict[str(list)] =i["hr_account"]
            self.data_tree.insert('', 'end', values=list)
        print(self.hr_dict)


    # 双击HR聊天,调取聊天室,如果切换了聊天对象，则清空收消息框的内容。提示与谁聊天中
    def treeviewClick(self, event):
        for item in self.data_tree.selection():
            self.choose_hr = self.data_tree.item(item, "values")
        print(self.choose_hr)
        if self.chat_info != self.choose_hr:
            # data = {"request_type": "p_get_record", "data":
            #     {"From": self.choose_info[4], "To": self.account}}
            # tip = "与%s沟通中..." % self.choose_info[4]
            # self.tip_chat = Label(self.window, text=tip, font=("黑体", 15)).place(x=700, y=120)
            # self.chat_sock.send(json.dumps(data).encode())
            self.text_msglist.delete('0.0', END)
            self.chat_info = self.choose_hr

    # 发送聊天信息，不能发送空内容，发送From,To,时间,内容到服务器
    def send_chatmsg(self):
        if self.text_msg.get("0.0", END) == "\n":
            tkinter.messagebox.showinfo(title='Error', message='不能发送空内容')
        else:
            c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
            data = {"request_type": "p_send_msg", "data":
                {"From": self.account, "To": self.chat_info[4], "send_time": c_time,
                 "send_content": self.text_msg.get("0.0", END)}}
            # self.chat_sock.send(json.dumps(data).encode())
            # print(data)
            self.deal_send(c_time)

    # 处理发送聊天框，发送完内容，发送框内清空,把自己发的消息打印到收消息框
    def deal_send(self, c_time):
        self.text_msglist.tag_config("green", foreground='green')
        msg_content = "我 " + c_time
        self.text_msglist.insert(END, msg_content, 'green')
        self.text_msglist.insert(END, self.text_msg.get("0.0", END))
        self.text_msglist.see(END)
        self.text_msg.delete('0.0', END)

    def run(self):
        Receive(self.text_msglist, self.chat_sock)

    def user_quit(self):
        self.window.destroy()
        hj_sock.close()
        self.chat_sock.close()


# 个人信息提交界面
class PersonalInfo:

    def __init__(self, master, account):
        self.account = account
        self.window = Toplevel(master)
        self.window.title('Complete Personal Information')
        self.width = 600
        self.height = 400
        self.resume_path = Entry(self.window, width='20', font=("黑体", 15))
        self.person_name = StringVar()
        self.expected_salary = StringVar()
        self.expected_position = StringVar()
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
        Entry(self.window, textvariable=self.expected_position, font=("黑体", 15)).place(x=250, y=160)
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

    # 确认提交个人信息,包括简历
    def submit_info(self):
        wanted_salary = self.expected_salary.get()
        wanted_position = self.expected_position.get()
        name = self.person_name.get()
        data = {"request_type": "p_submit_info", "data":
            {"account": self.account, "name": name, "wanted_salary": wanted_salary,
             "wanted_position": wanted_position, "resume": self.resume_conent}}
        print(data)
        print(json.dumps(data))
        hj_sock.send(json.dumps(data).encode())
        self.confirm_submit()

    # 确认是否提交成功
    def confirm_submit(self):
        data = hj_sock.recv(1024).decode()
        if data == "submit_info_success":
            tkinter.messagebox.showinfo(title='信息提交', message='提交成功')
            self.window.destroy()
        if data == "submit_info_failed":
            tkinter.messagebox.showinfo(title='信息提交', message='提交失败')

    # 选择简历文件
    def select_file(self):
        selectfile = tkinter.filedialog.askopenfilename()
        self.resume_path.insert(0, selectfile)
        self.read_resume(selectfile)

    # 读取选择文件中的内容
    def read_resume(self, file_path):
        f = open(file_path, "rb")
        self.resume_conent = f.read().decode()

    def user_quit(self):
        self.window.destroy()


# 企业登陆界面
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
        else:
            data = {"request_type": "e_login_verification", "data": {"account": user_name, "password": user_pwd}}
            hj_sock.send(json.dumps(data).encode())
            self.check_login()

    # 接收服务器消息，账号是否存在，密码是否正确，无误就弹出个人操作页面。
    def check_login(self):
        data = hj_sock.recv(1024).decode()
        if data == "user_not_exist":
            tkinter.messagebox.showinfo(title='Hello Job', message='账号不存在')
        elif data == "password_error":
            tkinter.messagebox.showinfo(title='Hello Job', message='密码错误')
        elif data == "allow_login":
            login_account = self.var_usr_name.get()
            self.window.destroy()
            global eview_tk
            eview_tk = Tk()
            client = EnterpriseView(eview_tk, login_account)
            client.start()
            eview_tk.mainloop()

    def user_quit(self):
        self.window.destroy()
        hj_sock.close()


# 企业操作界面
class EnterpriseView(Thread):
    ADDR = ('127.0.0.1', 8401)
    chat_sock = socket(AF_INET, SOCK_DGRAM)

    def __init__(self, master, account):
        super().__init__()
        self.window = master
        self.window.title('Hello Job')
        self.width = 1200
        self.height = 800
        self.postion = StringVar()
        self.window_postion()
        self.control_layout()
        self.account = account
        self.chat_info = ""
        self.choose_info = ""

    def control_layout(self):
        Label(self.window, text='找人才，就来Hello Job!!!', font=("黑体", 25)).place(x=50, y=50)
        Label(self.window, text='期望职位:', font=("黑体", 15)).place(x=150, y=150)
        Label(self.window, text='薪资范围:', font=("黑体", 15)).place(x=350, y=150)
        Label(self.window, text='温馨提示：双击表中的求职者，可以直接与求职者沟通哦！', font=("黑体", 15)).place(x=100, y=450)
        self.tip_chat = Label(self.window, text='', font=("黑体", 15)).place(x=700, y=120)
        Entry(self.window, textvariable=self.postion, width=15, font=("黑体", 15)).place(x=150, y=180)
        self.salary_range = ttk.Combobox(self.window, width=15, font=("黑体", 15))
        self.salary_range.pack()
        self.salary_range.place(x=350, y=180)
        self.salary_range['value'] = ('0 - 5000', '5000 - 10000', '10000 - 20000', '20000以上')
        Button(self.window, text="发布职位", command=self.complete_postion, font=("黑体", 15)).place(x=900, y=50)
        Button(self.window, text="查询", command=self.find_applicant, font=("黑体", 15)).place(x=600, y=160)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=1050, y=50)
        self.frame = Frame(self.window)
        self.frame.place(x=50, y=240, width=650, height=200)
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.title = ['1', '2', '3', '4']
        self.data_tree = ttk.Treeview(self.frame, columns=self.title,
                                      yscrollcommand=self.scrollbar.set,
                                      show='headings')
        self.data_tree.column('1', width=100)
        self.data_tree.column('2', width=150)
        self.data_tree.column('3', width=150)
        self.data_tree.column('4', width=150)
        self.data_tree.heading('1', text='姓名')
        self.data_tree.heading('2', text='邮箱')
        self.data_tree.heading('3', text='期望职位')
        self.data_tree.heading('4', text='期望薪资')
        self.scrollbar.config(command=self.data_tree.yview)
        self.data_tree.pack(side=LEFT, fill=Y)
        self.data_tree.bind('<Double-1>', self.treeviewClick)
        self.text_msglist = Text(self.window, width=65, height=23, bg='white')
        self.text_msglist.place(x=700, y=150)
        self.text_msglist.tag_config("green", foreground='green')
        self.text_msg = Text(self.window, width=65, height=10, bg='white')
        self.text_msg.place(x=700, y=460)
        self.send_msg = Button(self.window, text="发送", command=self.send_chatmsg, font=("黑体", 15)).place(x=700, y=600)
        self.send_msg = Button(self.window, text="下载简历", command=self.download_resume, font=("黑体", 15)).place(x=800,
                                                                                                              y=600)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    # 填写发布职位的名称，薪资，职责
    def complete_postion(self):
        AddPosition(self.window, self.account)

    # 查询求职者，按照薪资和职位
    def find_applicant(self):
        postion_name = self.postion.get()
        salary_range = self.salary_range.get()
        if salary_range == "20000以上":
            data = {"request_type": "search_applicant", "data":
                {"wanted_position": postion_name,
                 "wanted_salary": 20000 - 999999}}
        else:
            data = {"request_type": "search_applicant", "data":
                {"wanted_position": postion_name,
                 "wanted_salary": salary_range}}
        hj_sock.send(json.dumps(data).encode())
        rec_data = hj_sock.recv(1024 * 1024).decode()
        print(rec_data)
        if rec_data == "get_applicant_failed":
            self.clear_data()
            tkinter.messagebox.showinfo(title='Hello Job', message='没有找到符合的求职者')
        elif rec_data == "get_applicant_success":
            self.clear_data()
            self.insert_result()

    # 在查询工作前先清空之前查询的结果
    def clear_data(self):
        x = self.data_tree.get_children()
        for item in x:
            self.data_tree.delete(item)

    # 将返回的结果写入列表
    def insert_result(self):
        rec_data = hj_sock.recv(1024 * 1024).decode()
        result = json.loads(rec_data)
        print(result)
        for i in result["data"]:
            list = [i['name'], i['account'], i['wanted_position'], i['wanted_salary']]
            self.data_tree.insert('', 'end', values=list)

    # 双击求职者聊天,调取聊天室,如果切换了聊天对象，则清空收消息框的内容。提示与谁聊天中
    def treeviewClick(self, event):
        for item in self.data_tree.selection():
            self.choose_info = self.data_tree.item(item, "values")
        print(self.choose_info)
        if self.chat_info != self.choose_info:
            data = {"request_type": "p_get_record", "data":
                {"From": self.choose_info[0], "To": self.account}}
            tip = "与%s沟通中..." % self.choose_info[0]
            self.tip_chat = Label(self.window, text=tip, font=("黑体", 15)).place(x=700, y=120)
            self.chat_sock.send(json.dumps(data).encode())
            self.text_msglist.delete('0.0', END)
            self.chat_info = self.choose_info

    # 下载简历
    def download_resume(self):
        data = {"request_type": "download_resume", "data":
            {"account": self.choose_info[1]}}
        hj_sock.send(json.dumps(data).encode())
        save_path = tkinter.filedialog.asksaveasfilename(title='保存文件')
        print(save_path)
        rec_data = hj_sock.recv(1024 * 1024).decode()
        if rec_data == "no_resume":
            tkinter.messagebox.showinfo(title='Error', message='改求职者没有上传简历')
        else:
            with open(save_path, "wb") as f:
                f.write(rec_data.encode())

    # 发送聊天信息，不能发送空内容，发送From,To,时间,内容到服务器
    def send_chatmsg(self):
        if self.text_msg.get("0.0", END) == "\n":
            tkinter.messagebox.showinfo(title='Error', message='不能发送空内容')
        else:
            c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
            data = {"request_type": "send_msg", "data":
                {"From": self.account, "To": self.chat_info[1], "send_time": c_time,
                 "send_content": self.text_msg.get("0.0", END)}}
            self.chat_sock.sendto(json.dumps(data).encode(), ADDR)
            print(data)
            self.deal_send(c_time)

    # 处理发送聊天框，发送完内容，发送框内清空,把自己发的消息打印到收消息框
    def deal_send(self, c_time):
        self.text_msglist.tag_config("green", foreground='green')
        msg_content = "我 " + c_time
        self.text_msglist.insert(END, msg_content, 'green')
        self.text_msglist.insert(END, self.text_msg.get("0.0", END))
        self.text_msglist.see(END)
        self.text_msg.delete('0.0', END)

    def run(self):
        data = {'request_type': "login_chat", "account": self.account}
        self.chat_sock.sendto(json.dumps(data).encode(), ADDR)
        Receive(self.text_msglist, self.chat_sock)

    def user_quit(self):
        self.window.destroy()
        hj_sock.close()
        self.chat_sock.close()


# 添加职位
class AddPosition:

    def __init__(self, master, account):
        self.account = account
        self.window = Toplevel(master)
        self.window.title('Complete Personal Information')
        self.width = 600
        self.height = 400
        self.position = StringVar()
        self.duties = StringVar()
        self.salary = StringVar()
        self.control_layout()
        self.window_postion()

    def control_layout(self):
        Label(self.window, text='岗位名称', font=("黑体", 15)).place(x=150, y=80)
        Label(self.window, text='岗位职责', font=("黑体", 15)).place(x=150, y=120)
        Label(self.window, text='岗位薪资', font=("黑体", 15)).place(x=150, y=160)
        Entry(self.window, textvariable=self.position, font=("黑体", 15)).place(x=250, y=80)
        Entry(self.window, textvariable=self.duties, font=("黑体", 15)).place(x=250, y=120)
        Entry(self.window, textvariable=self.salary, font=("黑体", 15)).place(x=250, y=160)
        Button(self.window, text="提交", command=self.submit_position, font=("黑体", 15)).place(x=250, y=280)
        Button(self.window, text="退出", command=self.user_quit, font=("黑体", 15)).place(x=350, y=280)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    # 确认发布岗位信息
    def submit_position(self):
        salary = self.salary.get()
        duties = self.duties.get()
        position = self.position.get()
        data = {"request_type": "add_position", "data":
            {"account": self.account, "position": position, "duties": duties,
             "salary": salary}}
        hj_sock.send(json.dumps(data).encode())
        self.confirm_add()

    # 确认是否提交成功
    def confirm_add(self):
        data = hj_sock.recv(1024).decode()
        if data == "add_position_success":
            tkinter.messagebox.showinfo(title='Hello Job', message='发布职位成功')
            self.window.destroy()
        elif data == "add_position_failed":
            tkinter.messagebox.showinfo(title='Hello Job', message='发布职位失败')

    def user_quit(self):
        self.window.destroy()


# 收取聊天信息
class Receive():

    def __init__(self, text_msglist, chat_sock):

        while True:
            try:
                data = chat_sock.recvfrom(1024*1024).decode()
                rec_data = json.loads(data)
                record_from = "%s %s\n" % (rec_data["from"], rec_data["send_time"])
                text_msglist.tag_config("green", foreground='green')
                text_msglist.insert(END, record_from, 'green')
                text_msglist.insert(END, "%s \n" % rec_data["send_content"])
            except:
                break


HomePage(root)
# PersonalView(root, "asd")
# PersonalInfo(root,"asd")
# ChatClient(root,"asd","asd")
root.mainloop()
