"""
window
===============================================================================
"""
import wx
from wx.lib.gizmos.dynamicsash import DynamicSashWindow

from wbBase.document.notebook import DocumentPageMixin

from .control import TextDocEditCtrl


class TextWindow(DynamicSashWindow, DocumentPageMixin):
    def __init__(self, parent, doc, view):
        pos = wx.DefaultPosition
        size = wx.DefaultSize
        style = wx.CLIP_CHILDREN | wx.BORDER_NONE
        name = self.__class__.__name__
        DynamicSashWindow.__init__(self, parent, wx.ID_ANY, pos, size, style, name)
        DocumentPageMixin.__init__(self, doc, view)
        self.editor = TextDocEditCtrl(self)  # , doc=doc)
        # self.editor.textWin = self
        ## Connect Events
        # self.Bind(wx.EVT_SET_FOCUS, self.on_SET_FOCUS)

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.title)

    def SetText(self, text):
        try:
            self.editor.SetText(text.decode("utf-8"))
        except UnicodeDecodeError:
            self.editor.SetText(text.decode("cp1252"))

    @property
    def modified(self):
        return self.editor.GetModify()

    @modified.setter
    def modified(self, modified):
        self.editor.SetModify(modified)

        # def on_SET_FOCUS(self, event):
        # 	print('TextWindow.on_SET_FOCUS()')
        # 	self.editor.SetFocus()
