"""
xml
===============================================================================

Implementation of document template and configuration for
XML text files.
"""
import wx
import wx.stc as stc

from wbBase.control.textEditControl import XmlTextEditConfig
from . import PlainTextTemplate
from ..config import TextDocPreferencesBase

docTypeName = "XML Text"


class XMLTextPreferences(TextDocPreferencesBase):
    name = docTypeName


class XMLTextTemplate(PlainTextTemplate):
    def __init__(self, manager):
        PlainTextTemplate.__init__(self, manager)
        self._description = "XML Text File"
        self._fileFilter = "*.xml;*.xsd"
        self._defaultExt = ".xml"
        self._docTypeName = docTypeName
        self._icon = wx.ArtProvider.GetBitmap("HTML_FILE", wx.ART_FRAME_ICON)
        self.lexer = stc.STC_LEX_XML
        self.properties = {
            "fold": "1",
            "fold.html": "1",
            "lexer.xml.allow.scripts": "0",
        }
        self.commentPattern = ("<!--", "-->")
        self.editorConfig = XmlTextEditConfig(self)
        self.editorConfig.load()

