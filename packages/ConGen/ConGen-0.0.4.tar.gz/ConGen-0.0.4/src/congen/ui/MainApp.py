import wx

from ui.MainFrame import MainFrame


class MainApp(wx.App):
    def OnInit(self):
        frame = MainFrame("Test")
        frame.Show(True)
        return True
