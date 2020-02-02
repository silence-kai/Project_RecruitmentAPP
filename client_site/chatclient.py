from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import json
import time
from threading import Thread


# 收消息
class Receive():
    def __init__(self, client_sock, text_msglist):
        # data = {"request_type": "p_get_record"}
        while True:
            try:
                # client_sock.send(json.dumps(data).encode())
                data = client_sock.recv(1024 * 1024).decode()
                rec_data = json.loads(data)
                record_from = "%s %s\n" % (rec_data["from"], rec_data["send_time"])
                text_msglist.tag_config("green", foreground='green')
                text_msglist.insert(END, record_from, 'green')
                text_msglist.insert(END, "%s \n" % rec_data["send_content"])
            except:
                break


# 客户端聊天室
class ChatClient(Thread):

    def __init__(self, master, account, chat_info, client_sock):
        super().__init__()
        self.chat_info = chat_info
        self.account = account
        # self.window = master
        self.window = Toplevel(master)
        # self.window.title('%s' % (self.chat_info[4]))
        self.width = 600
        self.height = 600
        self.control_layout()
        self.window_postion()
        self.client_sock = client_sock
        time.sleep(2)
        # self.recv_chatmsg()

    def control_layout(self):
        self.text_msglist = Text(self.window, width=80, height=23, bg='white')
        self.text_msglist.place(x=20, y=20)
        self.text_msglist.tag_config("green", foreground='green')
        self.text_msg = Text(self.window, width=80, height=10, bg='white')
        self.text_msg.place(x=20, y=350)
        Button(self.window, text="关闭", command=self.user_quit, font=("黑体", 15)).place(x=200, y=520)
        self.send_msg = Button(self.window, text="发送", command=self.send_chatmsg, font=("黑体", 15)).place(x=350, y=520)

    def window_postion(self):
        alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
            (self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

    # 发送消息，判断是否内容为空，把输入框的内容打印在聊天窗口上，并清空输入框，发送给服务发送者，接收者，时间，内容。
    def send_chatmsg(self):
        if self.text_msg.get("0.0", END) == "\n":
            tkinter.messagebox.showinfo(title='Error', message='不能发送空内容')
        else:
            c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
            data = {"request_type": "p_send_msg", "data":
                {"From": self.account, "To": "self.chat_info[4]", "send_time": c_time,
                 "send_content": self.text_msg.get("0.0", END)}}
            self.client_sock.send(json.dumps(data).encode())
            print(data)
            self.deal_text(c_time)

    # 处理会话框，发送后自动清空输入框，将输入框的内容打印到对话框上
    def deal_text(self, c_time):
        self.text_msglist.tag_config("green", foreground='green')
        msg_content = "我 " + c_time
        self.text_msglist.insert(END, msg_content, 'green')
        self.text_msglist.insert(END, self.text_msg.get("0.0", END))
        self.text_msglist.see(END)
        self.text_msg.delete('0.0', END)

    def run(self):
        Receive(self.client_sock, self.text_msglist)

    def user_quit(self):
        self.window.destroy()

