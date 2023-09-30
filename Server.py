import socketserver
import pickle
import time
import json

# 参量及全局变量声明
# 传输上限
buf_size = 2048
# 绑定服务器的ip地址和端口
ip_server = ('127.0.0.1', 8000)
# 接收的聊天信息记录
msg_dict = {}
# 当前用户列表
client_list = {}
# 当前收到信息归类标识
tg = '0'
# 登录错误标识
log_err = '0'
# 本地用户名
local = 'Server'
# 当前处理的用户
cur_user = ''


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


# 制作数据包
def create_msg(tg_temp, ms):
    msg_temp = Mess()
    # 服务器发往客户端的登录类信息
    if tg_temp == '0':
        if ms == '0':
            # 正常登录
            msg_temp.tag = '00'
        elif ms == '1':
            # 登录出错
            msg_temp.tag = '01'
        msg_temp.username = local
        msg_temp.text = cur_user
        msg_temp.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg_temp.addr = '0.0.0.0'
    # 服务器发往客户端的聊天类信息
    if tg_temp == '1':
        msg_temp.tag = '1'
        msg_temp.text = ms
        msg_temp.username = cur_user
        msg_temp.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg_temp.addr = '0.0.0.0'
    # 服务器发往客户端的用户列表
    if tg_temp == '2':
        msg_temp.tag = '2'
        msg_temp.text = ms
        msg_temp.username = local
        msg_temp.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg_temp.addr = '0.0.0.0'
    return msg_temp


# 接收函数
def rcv(msg):
    global tg, log_err, cur_user

    # 接收到登录类信息
    if msg.tag == '0':
        cur_user = msg.username
        # 检查是否已有此用户名
        if cur_user not in client_list:
            log_err = '0'
        else:
            log_err = '1'
    # 接收到聊天类信息
    if msg.tag == '1':
        # 储存更新聊天信息
        msg_dict.update({f'{msg.username}({msg.time})': f'\n\t{msg.text}'})


# 继承服务器处理信息的类
class Group(socketserver.BaseRequestHandler):

    def handle(self):
        global tg, log_err, client_list

        while True:
            # 接收客户端信息
            rcv_data = pickle.loads(self.request.recv(buf_size))
            # 分类、初步处理客户端信息
            rcv(rcv_data)

            # 登录部分处理
            if rcv_data.tag == '0':
                # 登录验证
                mg = create_msg('0', log_err)
                self.request.sendall(pickle.dumps(mg))
                if log_err == '0':
                    client_list.update({cur_user: self.request})

                # 发送聊天信息给所有客户端
                send_all_client('1')
                time.sleep(0.1)
                # 发送新用户列表给所有客户端
                send_all_client('2')
                # 登录成功，修改log_err
                log_err = '0'

            # 聊天部分处理
            if rcv_data.tag == '1':
                # 发送聊天信息给所有客户端
                send_all_client('1')

            # 用户退出处理
            if rcv_data.tag == '111':
                # 用户列表中清除退出用户
                client_list.pop(rcv_data.username)
                # 发送新用户列表给所有客户端
                send_all_client('2')


# 发送信息至每一个客户端
def send_all_client(tag):
    # 判断发送的是用户列表还是聊天信息，相应处理信息格式
    if tag == '2':
        info = list(client_list.keys())
    else:
        info = json.dumps(msg_dict)

    # 发送至每一个用户
    mg = create_msg(tag, info)
    for user in client_list:
        client_list.get(user).sendall(pickle.dumps(mg))


if __name__ == "__main__":
    # 定义服务器线程
    s = socketserver.ThreadingTCPServer(ip_server, Group)
    # 服务器启动
    s.serve_forever()
