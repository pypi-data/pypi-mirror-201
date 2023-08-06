"""
config
===============================================================================
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import wx.propgrid as pg
import wx.stc as stc
from wbBase.dialog.preferences import PreferencesPageBase

from .template import PlainTextTemplate
from .window import TextWindow

if TYPE_CHECKING:
    from wbBase.document.template import DocumentTemplate


class TextEditPreferences(PreferencesPageBase):
    def __init__(self, parent):
        PreferencesPageBase.__init__(self, parent)
        cfg = self.config

        self.Append(pg.PropertyCategory("Right Edege"))
        self.Append(
            pg.EnumProperty(
                "Edge Style",
                "EdgeStyle",
                ("None", "Line", "Background"),
                (stc.STC_EDGE_NONE, stc.STC_EDGE_LINE, stc.STC_EDGE_BACKGROUND),
                cfg.ReadInt("EdgeStyle", stc.STC_EDGE_LINE),
            )
        )
        self.Append(
            pg.IntProperty("Column", "EdgeColumn", cfg.ReadInt("EdgeColumn", 80))
        )

        for prop in self.Properties:
            if isinstance(prop, pg.IntProperty):
                self.SetPropertyEditor(prop.GetName(), "SpinCtrl")
        self.SetPropertyAttributeAll("UseCheckbox", True)

    def applyValues(self):
        self.saveValues()
        for doc in self.app.TopWindow.documentManager.documents:
            for view in doc.views:
                if isinstance(view.frame, TextWindow):
                    view.frame.editor.loadConfig()

    def saveValues(self):
        cfg = self.config
        values = self.GetPropertyValues()
        # Setup Edge Mode
        cfg.WriteInt("EdgeStyle", values["EdgeStyle"])
        cfg.WriteInt("EdgeColumn", values["EdgeColumn"])


class TextDocPreferencesBase(PreferencesPageBase):
    name = "undefined"  # <- Document Type Name

    def __init__(self, parent):
        PreferencesPageBase.__init__(self, parent)
        template = self.template
        if isinstance(template, PlainTextTemplate):
            template.editorConfig.appendProperties(self)

            for prop in self.Properties:
                if isinstance(prop, pg.IntProperty):
                    self.SetPropertyEditor(prop.GetName(), "SpinCtrl")
            self.SetPropertyAttributeAll("UseCheckbox", True)
            self.Bind(pg.EVT_PG_CHANGED, self.OnChanged)

    @property
    def template(self) -> Optional[DocumentTemplate]:
        return self.app.TopWindow.documentManager.FindTemplateByDocumentTypeName(
            self.name
        )

    def applyValues(self):
        template = self.template
        if isinstance(template, PlainTextTemplate):
            editorConfig = template.editorConfig
            editorConfig.getPropertyValues(self)

            documentManager = self.app.TopWindow.documentManager
            for doc in documentManager.documents:
                if doc.typeName == self.name:
                    for view in doc.views:
                        if isinstance(view.frame, TextWindow):
                            editorConfig.apply(view.frame.editor)

    def saveValues(self):
        template = self.template
        if isinstance(template, PlainTextTemplate):
            editorConfig = template.editorConfig
            editorConfig.getPropertyValues(self)
            editorConfig.save()

    def OnChanged(self, event):
        if event.PropertyName in ("font", "background"):
            for p in self.Properties:
                self.RefreshProperty(p)
        event.Skip()


class PlainTextPreferences(TextDocPreferencesBase):
    name = "PlainTextDocument"
