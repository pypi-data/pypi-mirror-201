"""
control
===============================================================================
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import wx
import wx.stc as stc
from wbBase.control.textEditControl import TextEditSashChild
from wbBase.document.view import View

if TYPE_CHECKING:
    from .document import TextDocument
    from .template import PlainTextTemplate
    from .view import TextView


class TextDocEditCtrl(TextEditSashChild):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.BORDER_NONE,
        name="TextDocEditCtrl",
    ):
        TextEditSashChild.__init__(self, parent, id, pos, size, style, name)
        self.useAutoIndent = False
        self.autoIndenter = None
        self.commentPattern = ()
        self.contextMenu = None
        self.loadConfig()
        self.Bind(wx.EVT_SET_FOCUS, self.on_FOCUS)
        self.Bind(wx.EVT_KEY_DOWN, self.on_KEY_DOWN)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_RIGHT_DOWN)
        self.Bind(stc.EVT_STC_CHANGE, self.on_CHANGE)
        self.Bind(stc.EVT_STC_URIDROPPED, self.on_URIDROPPED)

    def __repr__(self):
        return f'<TextDocEditCtrl for document "{self.document.printableName}">'

    # -----------------------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------------------

    @property
    def view(self) -> Optional[TextView]:
        obj = self.dyn_sash
        if hasattr(obj, "view") and isinstance(obj.view, View):
            return obj.view
        while hasattr(obj, "Parent") and obj.Parent is not None:
            if hasattr(obj, "view") and isinstance(obj.view, View):
                return obj.view
            else:
                obj = obj.Parent
        return None

    @property
    def document(self) -> Optional[TextDocument]:
        view = self.view
        if view:
            return view.document
        return None

    @property
    def template(self) -> Optional[PlainTextTemplate]:
        doc = self.document
        if doc:  # and isinstance(doc.template, PlainTextTemplate):
            return doc.template
        return None

    @property
    def plugin(self) -> str:
        """
        :return: Name of the plugin module to which this object belongs to.
        """
        if self.template:
            return self.template.plugin
        return ""

    @property
    def config(self):
        cfg = self.app.config
        cfg.SetPath(f"/Plugin/{self.plugin}/")
        return cfg

    # -----------------------------------------------------------------------------
    # public methods
    # -----------------------------------------------------------------------------

    def loadConfig(self):
        # Setup Edge Mode
        cfg = self.config
        self.SetEdgeMode(cfg.ReadInt("EdgeStyle", stc.STC_EDGE_LINE))
        self.SetEdgeColumn(cfg.ReadInt("EdgeColumn", 80))
        # todo: add useAutoIndent to config
        self.useAutoIndent = True
        self.loadTemplateConfig()

    def loadTemplateConfig(self):
        # apply defaults from template
        template = self.template
        if template:  # isinstance(template, PlainTextTemplate):
            template.editorConfig.apply(self)
            self.contextMenu = template.contextMenu(self)
            self.SetLexer(template.lexer)
            for i, keyWords in enumerate(template.keyWords):
                self.SetKeyWords(i, keyWords)
            for name, value in template.properties.items():
                self.SetProperty(name, value)

            self.autoIndenter = template.autoIndenter
            self.indentKeywords = template.indentKeywords
            self.unindentKeywords = template.unindentKeywords
            self.commentPattern = template.commentPattern

    def AutoIndent(self):
        if self.autoIndenter:
            txt = self.autoIndenter(self, self.GetCurrentPos(), self.indentChar)
            txt = txt.replace("\n", self.EOLChar)
            self.AddText(txt)
            self.EnsureCaretVisible()

    def Comment(self, start, end, uncomment=False):
        """(Un)Comments a line or a selected block of text in a document.
        @param start: begining line (int)
        @param end: end line (int)
        @keyword uncomment: uncomment selection
        """
        if len(self.commentPattern):
            sel = self.GetSelection()
            c_start = self.commentPattern[0]
            c_end = ""
            if len(self.commentPattern) > 1:
                c_end = self.commentPattern[1]

                # Modify the selected line(s)
            self.BeginUndoAction()
            nchars = 0
            try:
                lines = range(end, start - 1, -1)
                for line_num in lines:
                    lstart = self.PositionFromLine(line_num)
                    lend = self.GetLineEndPosition(line_num)
                    text: str = self.GetTextRange(lstart, lend)
                    tmp = text.strip()
                    if len(tmp):
                        if uncomment:
                            if tmp.startswith(c_start):
                                text = text.replace(c_start, "", 1)
                            if c_end and tmp.endswith(c_end):
                                text = text.replace(c_end, "", 1)
                            nchars = nchars - len(c_start + c_end)
                        else:
                            text = c_start + text + c_end
                            nchars = nchars + len(c_start + c_end)

                        self.SetTargetStart(lstart)
                        self.SetTargetEnd(lend)
                        self.ReplaceTarget(text)
            finally:
                self.EndUndoAction()
                if sel[0] != sel[1]:
                    self.SetSelection(sel[0], sel[1] + nchars)
                else:
                    if len(self.commentPattern) > 1:
                        nchars = nchars - len(self.commentPattern[1])
                    self.GotoPos(sel[0] + nchars)

                # -----------------------------------------------------------------------------
                # Event handler
                # -----------------------------------------------------------------------------

    def on_FOCUS(self, event):
        # print('TextDocEditCtrl.on_FOCUS()')
        self.dyn_sash.editor = self
        if self.view:
            self.view.Activate()
            wx.CallAfter(self.SetFocus)
        event.Skip()

    def on_KEY_DOWN(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            if self.useAutoIndent:
                if self.GetSelectedText():
                    self.CmdKeyExecute(stc.STC_CMD_NEWLINE)
                else:
                    self.AutoIndent()
            else:
                event.Skip()
        else:
            event.Skip()

    def on_RIGHT_DOWN(self, event):
        if self.contextMenu is not None:
            self.contextMenu.UpdateUI()
            self.PopupMenu(self.contextMenu)
        else:
            event.Skip()

    def on_CHANGE(self, event):
        # print(f'TextEditCtrl.on_CHANGE()')
        data = self.GetTextRaw()
        if self.document and data != self.document._data:
            self.document._data = data
            self.document.modified = True
            self.document.UpdateAllViews(self.view, ["modify"])
            # self.view.OnUpdate(self, ['modify'])

    def on_URIDROPPED(self, event):
        for n in dir(event):
            print(n)
