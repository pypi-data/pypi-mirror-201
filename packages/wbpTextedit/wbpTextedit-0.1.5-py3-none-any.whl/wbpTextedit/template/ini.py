"""
ini
===============================================================================

Implementation of document template and configuration for
ini-style configuration files.
"""
import wx
import wx.stc as stc

docTypeName = "Config File"

from wbBase.control.textEditControl import TextEditConfig

from . import PlainTextTemplate
from ..config import TextDocPreferencesBase


class IniTextEditConfig(TextEditConfig):
    def __init__(self, parent):
        super().__init__(parent)
        self.syntax["STC_PROPS_DEFAULT"] = "fore:black,back:white"
        self.syntax["STC_PROPS_SECTION"] = "fore:#000000"
        self.syntax["STC_PROPS_KEY"] = "fore:#000000"
        self.syntax["STC_PROPS_DEFVAL"] = "fore:#000000"
        self.syntax["STC_PROPS_COMMENT"] = "fore:#000000"
        self.syntax["STC_PROPS_ASSIGNMENT"] = "fore:#000000"


class IniTextPreferences(TextDocPreferencesBase):
    name = docTypeName


class IniTextTemplate(PlainTextTemplate):
    def __init__(self, manager):
        PlainTextTemplate.__init__(self, manager)
        self._description = "Config Text File"
        self._fileFilter = "*.ini;*.cfg"
        self._defaultExt = ".ini"
        self._docTypeName = docTypeName
        self._icon = wx.ArtProvider.GetBitmap("HTML_FILE", wx.ART_FRAME_ICON)
        self.lexer = stc.STC_LEX_PROPERTIES
        self.properties = {
            "fold": "1",
            #'fold.html' : '1',
            #'lexer.xml.allow.scripts' : '0',
        }
        self.commentPattern = ("#",)
        self.editorConfig = IniTextEditConfig(self)
        self.editorConfig.load()
