import wx


class ValueChoice(wx.Choice):
    def __init__(self, parent, value_list):
        assert value_list is not None
        self.value_list = value_list
        super().__init__(parent, choices=["None", *[str(value) for value in self.value_list]])
        self.Select(0)

    def GetValue(self):
        if self.GetSelection() == 0:
            return None
        else:
            return self.value_list[self.GetSelection() - 1]

    def SetValue(self, value):
        self.Select([None, *self.value_list].index(value))