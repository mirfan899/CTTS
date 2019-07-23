# inspired from: https://wiki.wxpython.org/ProportionalSplitterWindow

import wx

class SplitterPanel( wx.SplitterWindow ):
    def __init__(self,parent,proportion=0.66):
            wx.SplitterWindow.__init__(self,parent,-1,wx.Point(0,0),size=wx.DefaultSize,style=wx.SP_NOBORDER)
            self.proportion = proportion
            if not 0 < self.proportion < 1:
                    raise ValueError("proportion value for ProportionalSplitter must be between 0 and 1.")
            self.ResetSash()
            self.Bind(wx.EVT_SIZE, self.OnReSize)
            self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged)
            ##hack to set sizes on first paint event
            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.firstpaint = True

    def SplitHorizontally(self, win1, win2):
            if self.GetParent() is None: return False
            return wx.SplitterWindow.SplitHorizontally(self, win1, win2,
                    int(round(self.GetParent().GetSize().GetHeight() * self.proportion)))

    def SplitVertically(self, win1, win2):
            if self.GetParent() is None: return False
            return wx.SplitterWindow.SplitVertically(self, win1, win2,
                    int(round(self.GetParent().GetSize().GetWidth() * self.proportion)))

    def GetExpectedSashPosition(self):
            if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                    tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().height)
            else:
                    tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().width)
            return int(round(tot * self.proportion))

    def ResetSash(self):
            self.SetSashPosition(self.GetExpectedSashPosition())

    def OnReSize(self, event):
            "Window has been resized, so we need to adjust the sash based on self.proportion."
            self.ResetSash()
            event.Skip()

    def OnSashChanged(self, event):
            "We'll change self.proportion now based on where user dragged the sash."
            pos = float(self.GetSashPosition())
            if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                    tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().height)
            else:
                    tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().width)
            self.proportion = pos / tot
            event.Skip()

    def OnPaint(self,event):
            if self.firstpaint:
                    if self.GetSashPosition() != self.GetExpectedSashPosition():
                            self.ResetSash()
                    self.firstpaint = False
            event.Skip()

