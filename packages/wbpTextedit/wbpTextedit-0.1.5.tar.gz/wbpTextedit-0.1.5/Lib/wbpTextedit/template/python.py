"""
python
===============================================================================

Implementation of document template and configuration for
Python Script text files.
"""
from keyword import kwlist
import __main__

import wx
import wx.stc as stc

from wbBase.control.textEditControl import PyTextEditConfig
from . import PlainTextTemplate
from . import ContextMenu as ContextMenuBase
from ..config import TextDocPreferencesBase

docTypeName = "Python Script"


def PythonAutoIndeter(editor, pos, indentChar):
    line = editor.GetCurrentLine()
    spos = editor.PositionFromLine(line)
    text = editor.GetTextRange(spos, pos)
    epos = editor.GetLineEndPosition(line)
    inspace = text.isspace()
    if inspace:  # Cursor is in the indent area somewhere
        return u"\n" + text
    if not len(text):
        return u"\n"  # Cursor is in column 0 and just return newline.
    indent = editor.GetLineIndentation(line)
    if indentChar == u"\t":
        tabw = editor.GetTabWidth()
    else:
        tabw = editor.GetIndent()
    i_space = int(round(indent / tabw))
    end_spaces = (indent - (tabw * i_space)) * u" "
    tokens = list(filter(None, text.strip().split()))
    if tokens and not inspace:
        if tokens[-1].endswith(u":"):
            if tokens[0].rstrip(u":") in editor.indentKeywords:
                i_space += 1
        elif tokens[-1].endswith(u"\\"):
            i_space += 1
        elif tokens[0] in editor.unindentKeywords:
            i_space = max(i_space - 1, 0)
    rval = u"\n" + (indentChar * i_space) + end_spaces
    if inspace and indentChar != u"\t":
        rpos = indent - (pos - spos)
        if rpos < len(rval) and rpos > 0:
            rval = rval[:-rpos]
        elif rpos >= len(rval):
            rval = u"\n"
    return rval


class ContextMenu(ContextMenuBase):
    def __init__(self, editor, title=""):
        ContextMenuBase.__init__(self, editor, title)


class PythonTextPreferences(TextDocPreferencesBase):
    name = docTypeName


# "tab.timmy.whinge.level",
# "For Python code, checks whether indenting is consistent. "
# "The default, 0 turns off indentation checking, "
# "1 checks whether each line is potentially inconsistent with the previous line, "
# "2 checks whether any space characters occur before a tab character in the indentation, "
# "3 checks whether any spaces are in the indentation, and "
# "4 checks for any tab characters in the indentation. "
# "1 is a good level to use.");


class PythonTextTemplate(PlainTextTemplate):
    def __init__(self, manager):
        PlainTextTemplate.__init__(self, manager)
        self._description = "Python Source File"
        self._fileFilter = "*.py;*.pyw"
        self._defaultExt = ".py"
        self._docTypeName = docTypeName
        self._icon = wx.ArtProvider.GetBitmap("PYTHON_FILE", wx.ART_FRAME_ICON)
        self.lexer = stc.STC_LEX_PYTHON
        self.properties = {
            "fold": "1",
            "fold.compact": "1",
            "fold.quotes.python": "1",
            "lexer.python.literals.binary": "1",  #      Set to 0 to not recognise Python 3 binary and octal literals: 0b1011 0o712.
            "lexer.python.strings.u": "1",  #            Set to 0 to not recognise Python Unicode literals u"x" as used before Python 3.
            "lexer.python.strings.b": "1",  #            Set to 0 to not recognise Python 3 bytes literals b"x".
            "lexer.python.strings.f": "1",  #            Set to 0 to not recognise Python 3.6 f-string literals f"var={var}".
            "lexer.python.strings.over.newline": "0",  # Set to 1 to allow strings to span newline characters.
            "lexer.python.keywords2.no.sub.identifiers": "0",  # When enabled, it will not style keywords2 items that are used as a sub-identifier.
            # Example: when set, will not highlight "foo.open" when "open" is a keywords2 item.
            "lexer.python.unicode.identifiers": "1",  #  Set to 0 to not recognise Python 3 unicode identifiers.
            "tab.timmy.whinge.level": "2",
        }
        self.autoIndenter = PythonAutoIndeter
        keywords = " ".join(kwlist)
        builtins = " ".join(
            dir(__main__.__dict__["__builtins__"]) + ["__main__", "__class__"]
        )
        self.keyWords = (keywords, builtins)
        self.indentKeywords = (
            "def",
            "if",
            "elif",
            "else",
            "for",
            "with",
            "while",
            "class",
            "try",
            "except",
            "finally",
        )
        self.unindentKeywords = (
            "return",
            "raise",
            "break",
            "continue",
            "pass",
            "exit",
            "quit",
        )
        self.commentPattern = ("#",)
        self.editorConfig = PyTextEditConfig(self)
        self.editorConfig.load()

