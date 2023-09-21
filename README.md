# Multiplayer LAN chat room-Based on socket and wx
 简易带gui的局域网聊天室

    1、需要自行下载wx库,在命令行输入pip install wxPython
    2、服务器默认IP为'127.0.0.1'即本地，若要服务器和客户端在局域网不同主机上连接，需要将Server.py的ip_server和Client.py的ip_client修改为运行服务器的主机IP
    3、Client.py需要与support.py在一起（Client.py中import support），Server.py可以独自运行
    
