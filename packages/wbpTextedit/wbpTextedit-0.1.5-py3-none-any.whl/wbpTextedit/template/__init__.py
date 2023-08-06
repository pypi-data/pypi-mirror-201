"""
template
===============================================================================
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import wx
import wx.stc as stc
from wbBase.control.textEditControl import TextEditConfig
from wbBase.document.template import DEFAULT_TEMPLATE_FLAGS, DocumentTemplate

from ..document import TextDocument
from ..view import TextView

if TYPE_CHECKING:
    from ..control import TextDocEditCtrl


def DefaultAutoIndeter(editor: TextDocEditCtrl, pos: int, indentChar: str) -> str:
    """
    Default auto indenter for all text edit controls
    """
    rtxt = ""
    line = editor.GetCurrentLine()
    spos = editor.PositionFromLine(line)
    text = editor.GetTextRange(spos, pos)
    epos = editor.GetLineEndPosition(line)
    inspace = text.isspace()
    if inspace:  # Cursor is in the indent area somewhere
        return "\n" + text
    if not len(text):
        return "\n"  # Cursor is in column 0 and just return newline.
    indent = editor.GetLineIndentation(line)
    if indentChar == "\t":
        tabw = editor.GetTabWidth()
    else:
        tabw = editor.GetIndent()
    i_space = int(round(indent / tabw))
    ndent = "\n" + indentChar * i_space
    return ndent + ((indent - (tabw * i_space)) * " ")


class ContextMenu(wx.Menu):
    def __init__(self, editor: TextDocEditCtrl, title: str = ""):
        wx.Menu.__init__(self, title, style=0)
        self.editor = editor
        bmp = lambda artId: wx.ArtProvider.GetBitmap(
            artId, wx.ART_MENU, wx.Size(16, 16)
        )

        item = wx.MenuItem(self, wx.ID_INDENT, "Indent\tTab")
        item.Bitmap = bmp("wxART_INDENT")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.on_Indent, id=item.Id)
        self.Bind(wx.EVT_UPDATE_UI, self.on_UpdateIndent, id=item.Id)

        item = wx.MenuItem(self, wx.ID_UNINDENT, "Unindent\tShift+Tab")
        item.Bitmap = bmp("wxART_UNINDENT")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.on_Unindent, id=item.Id)
        self.Bind(wx.EVT_UPDATE_UI, self.on_UpdateIndent, id=item.Id)

        item = wx.MenuItem(self, wx.ID_ANY, "Comment")
        item.Bitmap = bmp("wxART_COMMENT")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.on_Comment, id=item.Id)
        self.Bind(wx.EVT_UPDATE_UI, self.on_UpdateComment, id=item.Id)

        item = wx.MenuItem(self, wx.ID_ANY, "Uncomment")
        item.Bitmap = bmp("wxART_UNCOMMENT")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.on_Uncomment, id=item.Id)
        self.Bind(wx.EVT_UPDATE_UI, self.on_UpdateComment, id=item.Id)

    def on_Indent(self, event):
        self.editor.CmdKeyExecute(stc.STC_CMD_TAB)

    def on_Unindent(self, event):
        self.editor.CmdKeyExecute(stc.STC_CMD_BACKTAB)

    def on_UpdateIndent(self, event: wx.UpdateUIEvent):
        selection = self.editor.GetSelection()
        start = self.editor.LineFromPosition(selection[0])
        end = self.editor.LineFromPosition(selection[1])
        event.Enable(start != end)

    def on_Comment(self, event):
        selection = self.editor.GetSelection()
        start = self.editor.LineFromPosition(selection[0])
        end = self.editor.LineFromPosition(selection[1])
        if end > start and self.editor.GetColumn(selection[1]) == 0:
            end = end - 1
        self.editor.Comment(start, end)

    def on_Uncomment(self, event):
        selection = self.editor.GetSelection()
        start = self.editor.LineFromPosition(selection[0])
        end = self.editor.LineFromPosition(selection[1])
        if end > start and self.editor.GetColumn(selection[1]) == 0:
            end = end - 1
        self.editor.Comment(start, end, True)

    def on_UpdateComment(self, event: wx.UpdateUIEvent):
        event.Enable(len(self.editor.commentPattern) > 0)


class PlainTextTemplate(DocumentTemplate):
    """
    Document template for Plain Text Documents.
    """
    def __init__(self, manager):
        description = "Plain Text Document"
        filter = "*.txt"
        dir = ""
        ext = ".txt"
        docTypeName = "PlainTextDocument"
        viewTypeName = "PlainTextView"
        docType = TextDocument
        viewType = TextView
        flags = DEFAULT_TEMPLATE_FLAGS
        icon = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_FRAME_ICON)
        DocumentTemplate.__init__(
            self,
            manager,
            description,
            filter,
            dir,
            ext,
            docTypeName,
            viewTypeName,
            docType,
            viewType,
            flags,
            icon,
        )
        self.lexer = stc.STC_LEX_NULL
        self.contextMenu = ContextMenu
        self.properties = {}
        self.autoIndenter = DefaultAutoIndeter
        self.keyWords = ()
        self.indentKeywords = ()
        self.unindentKeywords = ()
        self.commentPattern = ()
        self.editorConfig = TextEditConfig(self)
        self.editorConfig.load()
