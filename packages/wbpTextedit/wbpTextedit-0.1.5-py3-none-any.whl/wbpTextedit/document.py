"""
document
===============================================================================
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from wbBase.document import Document

if TYPE_CHECKING:
    from wbBase.document.template import DocumentTemplate


class TextDocument(Document):
    binaryData = True
    canReload = True

    def __init__(self, template: DocumentTemplate):
        Document.__init__(self, template)
        self._encoding = "utf-8"
