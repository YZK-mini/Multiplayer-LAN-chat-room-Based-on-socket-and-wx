import threading
import time
from socket import *
import pickle
import json
import support
import wx

# 参量及全局变量声明
# 连接的服务器ip及端口
ip_client = ('127.0.0.1', 8000)
# 传输上限
buf_size = 2048
# 用户列表
client_list = []
# 聊天信息
msg_dict = {}
# 变化前的用户列表
recent_list = []


# 登录窗口功能
class LLogin_window(support.login):
    def __init__(self, parent):
        support.login.__init__(self, parent)

    def close(self, event):
        # 调用Win的destroy函数
        Win.destroy()
        # 关闭套接字
        client.close()

    # 登录检查函数
    def log_check(self, event):
        # 获取输入的用户名
        cur_user = self.m_textCtrl8.GetValue()
        # 发送获取的用户名至服务器
        msg_send = Win.create_msg('0', cur_user)
        client.send(pickle.dumps(msg_send))


# 主窗口功能
class Main_window(support.main):
    global client_list, msg_dict, recent_list

    def __init__(self, parent):
        support.main.__init__(self, parent)

    def Text_send(self, event):
        # 获取输入框内的输入
        text = self.input_text.GetValue()
        # 将输入信息发送至服务器
        msg_send = Win.create_msg('1', text)
        client.send(pickle.dumps(msg_send))
        # 将输入框清空
        self.input_text.Clear()

    def list_client(self):
        # 清空当前在线用户窗口
        self.client_box.Clear()
        # 重新打印当前用户至用户窗口
        for client_name in client_list:
            temp = f"{client_name}\n"
            self.client_box.AppendText(text=temp)
        # 用户加入或离开相关提示语
        if len(client_list) > len(recent_list):
            # 显示欢迎新用户
            self.msg_box.AppendText(f'\n（欢迎 "{client_list[-1]}" 进入聊天室）')
        elif len(client_list) < len(recent_list):
            # 显示某用户离开
            self.msg_box.AppendText(f'\n（ "{(set(recent_list) - set(client_list)).pop()}" 离开了聊天室）')

    def list_msg(self):
        # 清空聊天窗口的旧信息
        self.msg_box.Clear()
        # 将聊天信息打印到聊天窗口
        for msg in msg_dict:
            temp = msg
            self.msg_box.AppendText(text=temp)
            self.msg_box.AppendText(text='\t')
            temp = msg_dict.get(msg)
            self.msg_box.AppendText(text=temp)
            self.msg_box.AppendText(text='\n')

    def close_win(self, event):
        # 调用Win的destroy函数
        Win.destroy()
        # 停止receiver线程
        receiver._running = False
        # 向服务器发送用户退出信息
        msg_send = Win.create_msg('111', '')
        client.send(pickle.dumps(msg_send))
        # 关闭套接字
        client.close()


class Windows_helper:
    def __init__(self):
        self.app = wx.App()
        self.login_frame = LLogin_window(None)
        self.main_frame = Main_window(None)
        self.local = ''
        self.local_ip = client.getsockname()[0]

    # 登录界面及主界面生成
    def login(self):
        # 显示登录界面
        self.login_frame.Show(True)
        # 隐藏聊天界面
        self.main_frame.Show(False)
        # 启动显示窗口的循环
        self.app.MainLoop()

    def warn(self):
        # 显示’用户名重复‘警告
        self.login_frame.m_staticText5.Show()

    # 主界面显示
    def main_window(self):
        # 隐藏登录界面
        self.login_frame.Show(False)
        # 显示聊天界面
        self.main_frame.Show(True)

    # 窗口关闭函数
    def destroy(self):
        # 删除登录界面
        self.login_frame.Destroy()
        # 删除聊天界面
        self.main_frame.Destroy()

    # 制作数据包
    def create_msg(self, tg, ms):
        # 将msg_temp定义为Mess类
        msg_temp = Mess()
        # 客户端发往服务器的登录类信息
        if tg == '0':
            msg_temp.tag = '0'
            msg_temp.username = ms
            msg_temp.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            msg_temp.addr = self.local_ip
        # 客户端发往服务器的聊天类信息
        if tg == '1':
            msg_temp.tag = '1'
            msg_temp.text = ms
            msg_temp.username = self.local
            msg_temp.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            msg_temp.addr = self.local_ip
        # 客户端退出的信息
        if tg == '111':
            msg_temp.tag = '111'
            msg_temp.username = self.local

        return msg_temp

    # 接收函数
    def rcv(self, msg):
        global msg_dict, client_list, recent_list
        # 登录复验（成功）
        if msg.tag == '00':
            # 储存用户名
            self.local = msg.text
            # 进入聊天界面
            self.main_window()
        # 登录复验(失败)
        elif msg.tag == '01':
            self.local = ''
            # 显示‘用户名重复’提示
            self.warn()
        # 接收到聊天信息
        elif msg.tag == '1':
            msg_dict = json.loads(msg.text)
            # 展示聊天信息
            self.main_frame.list_msg()
        # 接收到用户列表
        elif msg.tag == '2':
            recent_list = client_list
            client_list = msg.text
            # 展示用户列表
            self.main_frame.list_client()


# 规定数据包格式
class Mess:
    def __init__(self):
        # 数据包标识
        self.tag = ''
        # 数据包内容
        self.text = ''
        # 数据包发送者
        self.username = ''
        # 数据包来源地址
        self.addr = ''
        # 数据包发送时间
        self.time = ''


#  接收线程
class monitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global client
        # 循环不断地检测是否接收到数据包
        while True:
            msg_recv = pickle.loads(client.recv(buf_size))
            # 对数据包进行分析处理
            Win.rcv(msg_recv)


if __name__ == '__main__':
    # 定义套接字并连接到服务器
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(ip_client)
    # 设定receiver线程，并启动
    receiver = monitor()
    receiver.start()
    # 定义Win为Windows_helper类
    Win = Windows_helper()
    # 开始登录
    Win.login()
