import threading
import time
from socket import *
import pickle
import json
import support
import wx

# 参量及全局变量声明
ip_client = ('127.0.0.1', 8000)
buf_size = 2048
local = ''
client = socket(AF_INET, SOCK_STREAM)
client.connect(ip_client)
local_ip = client.getsockname()[0]
client_list = []  # 用户列表
msg_dict = {}  # 聊天信息
cur_user = ''


# 登录窗口功能
class LLogin_window(support.login):
    def __init__(self, parent):
        support.login.__init__(self, parent)

    def close(self, event):
        destroy()
        client.close()

    def log_check(self, event):
        global cur_user
        cur_user = self.m_textCtrl8.GetValue()
        # 登录端口
        msg_send = create_msg('0', cur_user)
        client.send(pickle.dumps(msg_send))


# 主窗口功能
class Main_window(support.main):
    global client_list, msg_dict

    def __init__(self, parent):
        support.main.__init__(self, parent)

    def Text_send(self, event):
        text = self.input_text.GetValue()
        msg_send = create_msg('1', text)
        client.send(pickle.dumps(msg_send))
        self.input_text.Clear()

    def list_client(self):
        self.client_box.Clear()
        print(client_list)
        for client_name in client_list:
            temp = f"{client_name}\n"
            self.client_box.AppendText(text=temp)

        self.msg_box.AppendText(f'\n（欢迎 "{client_list[-1]}" 进入聊天室）')

    def list_msg(self):
        self.msg_box.Clear()
        for msg in msg_dict:
            temp = msg
            self.msg_box.AppendText(text=temp)
            self.msg_box.AppendText(text='\t')
            temp = msg_dict.get(msg)
            self.msg_box.AppendText(text=temp)
            self.msg_box.AppendText(text='\n')

    def close_win(self, event):
        destroy()
        s._running = False
        msg_send = create_msg('111', '')
        client.send(pickle.dumps(msg_send))
        client.close()


# 登录界面及主界面生成
def login():
    global login_frame, main_frame, warn_frame

    app = wx.App()
    login_frame = LLogin_window(None)
    login_frame.Show(True)
    main_frame = Main_window(None)
    main_frame.Show(False)
    app.MainLoop()


def warn():
    global login_frame
    login_frame.m_staticText5.Show()


# 主界面显示
def main_window():
    global login_frame, main_frame

    login_frame.Show(False)
    main_frame.Show(True)


# 窗口关闭函数
def destroy():
    global login_frame, main_frame

    login_frame.Destroy()
    main_frame.Destroy()


# 规定数据包格式
class Mess:
    def __init__(self):
        self.tag = ''
        self.text = ''
        self.username = ''
        self.addr = ''
        self.time = ''


# 制作数据包
def create_msg(tg, ms):
    global local

    msg_temp = Mess()
    # 客户端发往服务器的登录类信息
    if tg == '0':
        msg_temp.tag = '0'
        msg_temp.username = ms
        msg_temp.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg_temp.addr = local_ip
    # 客户端发往服务器的聊天类信息
    if tg == '1':
        msg_temp.tag = '1'
        msg_temp.text = ms
        msg_temp.username = local
        msg_temp.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg_temp.addr = local_ip
    # 客户端退出的信息
    if tg == '111':
        msg_temp.tag = '111'
        msg_temp.username = local

    return msg_temp


# 接收函数
def rcv(msg):
    global local, msg_dict, client_list, main_frame
    # 登录复验
    if msg.tag == '00':
        local = msg.text
        main_window()
    # 登录复验
    elif msg.tag == '01':
        local = ''
        warn()
    # 接收到聊天信息
    elif msg.tag == '1':
        msg_dict = json.loads(msg.text)
        main_frame.list_msg()
    # 接收到用户列表
    elif msg.tag == '2':
        client_list = msg.text
        main_frame.list_client()


#  接收线程
class monitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global client

        while True:
            msg_recv = pickle.loads(client.recv(buf_size))
            rcv(msg_recv)


if __name__ == '__main__':
    msg1 = Mess()
    s = monitor()
    s.start()
    login()
