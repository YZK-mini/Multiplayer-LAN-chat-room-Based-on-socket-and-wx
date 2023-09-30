import wx
import wx.xrc


###########################################################################
# Class main
###########################################################################

class main(wx.Frame):

    def __init__(self, parent):

        # 创建main窗口，设置相关参数
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"聊天界面", pos=wx.DefaultPosition, size=wx.Size(685, 570),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetWindowStyle(self.GetWindowStyle() & ~wx.RESIZE_BORDER)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        fgSizer1 = wx.FlexGridSizer(2, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # 聊天信息框
        self.msg_box = wx.TextCtrl(self, wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 400),
                                   style=wx.TE_READONLY | wx.TE_MULTILINE)
        fgSizer1.Add(self.msg_box, 0, wx.ALL, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        # 用户列表显示框
        self.m_button4 = wx.Button(self, wx.ID_ANY, u"用户列表", wx.DefaultPosition, wx.Size(150, -1), 0)
        bSizer3.Add(self.m_button4, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)

        self.client_box = wx.TextCtrl(self, wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(150, 365),
                                      style=wx.TE_READONLY | wx.TE_MULTILINE)
        bSizer3.Add(self.client_box, 0, wx.RIGHT | wx.LEFT, 5)

        fgSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        # 用户输入框
        self.input_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(500, 100),
                                      wx.TE_PROCESS_ENTER | wx.TE_MULTILINE)
        fgSizer1.Add(self.input_text, 0, wx.ALL, 5)

        # ’发送‘按钮
        self.m_button3 = wx.Button(self, wx.ID_ANY, u"发送", wx.DefaultPosition, wx.Size(50, 100), 0)
        fgSizer1.Add(self.m_button3, 0, wx.ALL, 5)

        self.SetSizer(fgSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # 将关闭窗口与close_win绑定
        self.Bind(wx.EVT_CLOSE, self.close_win)
        # 将发送按钮与Text_send绑定
        self.m_button3.Bind(wx.EVT_BUTTON, self.Text_send)
        # 将回车键与Text_send绑定
        self.input_text.Bind(wx.EVT_TEXT_ENTER, self.Text_send)

    def __del__(self):
        pass

    def close_win(self, event):
        event.Skip()

    def Text_send(self, event):
        event.Skip()


###########################################################################
# Class login
###########################################################################

class login(wx.Frame):

    def __init__(self, parent):

        # 创建main窗口，设置相关参数
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"登录界面", pos=wx.DefaultPosition, size=wx.Size(400, 200),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetWindowStyle(self.GetWindowStyle() & ~wx.RESIZE_BORDER)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        gSizer4 = wx.GridSizer(0, 1, 0, 0)

        # 显示‘登录’字样
        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"登录", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        self.m_staticText5.SetFont(wx.Font(14, 74, 90, 92, False, "微软雅黑"))

        gSizer4.Add(self.m_staticText5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM, 5)

        bSizer8.Add(gSizer4, 1, wx.EXPAND, 5)

        gSizer6 = wx.GridSizer(0, 3, 0, 0)

        # 用户名输入框
        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"用户名:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        gSizer6.Add(self.m_staticText6, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.m_textCtrl8 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                       wx.TE_PROCESS_ENTER)
        gSizer6.Add(self.m_textCtrl8, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ‘用户名重复’提示
        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"用户名\n重复", wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTRE)
        self.m_staticText5.Wrap(-1)
        self.m_staticText5.SetFont(wx.Font(7, 70, 90, 90, False, "宋体"))
        self.m_staticText5.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.m_staticText5.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.m_staticText5.Hide()

        gSizer6.Add(self.m_staticText5, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer8.Add(gSizer6, 1, wx.EXPAND, 5)

        gSizer8 = wx.GridSizer(0, 1, 0, 0)

        # ‘登录’按钮
        self.m_button13 = wx.Button(self, wx.ID_ANY, u"登录", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer8.Add(self.m_button13, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer8.Add(gSizer8, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer8)
        self.Layout()

        self.Centre(wx.BOTH)

        # 将窗口关闭与close绑定
        self.Bind(wx.EVT_CLOSE, self.close)
        # 将登录按钮与log_check绑定
        self.m_button13.Bind(wx.EVT_BUTTON, self.log_check)
        # 将回车与log_check绑定
        self.m_textCtrl8.Bind(wx.EVT_TEXT_ENTER, self.log_check)

    def __del__(self):
        pass

    def close(self, event):
        event.Skip()

    def log_check(self, event):
        event.Skip()
