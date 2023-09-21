import socketserver
import pickle
import time
import json

buf_size = 2048
ip_server = ('127.0.0.1', 8000)
msg_dict = {}  # 接收的聊天信息记录
client_list = {}  # 当前用户列表
tg = '0'  # 当前收到信息归类标识
log_err = '0'  # 登录错误标识
local = 'Server'
cur_user = ''


class Mess:
    def __init__(self):
        self.tag = ''
        self.text = ''
        self.username = ''
        self.addr = ''
        self.time = ''


def create_msg(tg_temp, ms):
    msg_temp = Mess()
    # 服务器发往客户端的登录类信息
    if tg_temp == '0':
        if ms == '0':
            msg_temp.tag = '00'  # 正常登录
        elif ms == '1':
            msg_temp.tag = '01'  # 登录出错
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


def rcv(msg):
    global tg, log_err, cur_user
    # 接收到登录类信息
    if msg.tag == '0':
        cur_user = msg.username
        if cur_user not in client_list:
            log_err = '0'
        else:
            log_err = '1'
    # 接收到聊天类信息
    if msg.tag == '1':
        msg_dict.update({f'{msg.username}({msg.time})': f'\n\t{msg.text}'})


class Group(socketserver.BaseRequestHandler):
    def handle(self):
        global tg, log_err, client_list

        while True:
            rcv_data = pickle.loads(self.request.recv(buf_size))  # 接收客户端信息
            rcv(rcv_data)  # 分类、初步处理客户端信息
            # 登录部分处理
            if rcv_data.tag == '0':
                mg = create_msg('0', log_err)  # 登录验证
                self.request.sendall(pickle.dumps(mg))
                if log_err == '0':
                    client_list.update({cur_user: self.request})
                print(client_list)
                mg = create_msg('1', json.dumps(msg_dict))  # 发送聊天信息
                for user in client_list.keys():
                    client_list.get(user).sendall(pickle.dumps(mg))
                time.sleep(0.1)
                mg = create_msg('2', list(client_list.keys()))  # 发送用户列表
                for user in client_list.keys():
                    print(user)
                    client_list.get(user).sendall(pickle.dumps(mg))
                log_err = '0'

            # 聊天部分处理
            if rcv_data.tag == '1':
                mg = create_msg('1', json.dumps(msg_dict))  # 发送聊天信息
                for user in client_list:
                    client_list.get(user).sendall(pickle.dumps(mg))

            # 用户退出处理
            if rcv_data.tag == '111':
                client_list.pop(rcv_data.username)  # 用户列表中清除退出用户
                mg = create_msg('2', list(client_list.keys()))  # 发送用户列表
                for user in client_list:
                    client_list.get(user).sendall(pickle.dumps(mg))


if __name__ == "__main__":
    s = socketserver.ThreadingTCPServer(ip_server, Group)  # 定义服务器线程
    s.serve_forever()  # 服务器启动
