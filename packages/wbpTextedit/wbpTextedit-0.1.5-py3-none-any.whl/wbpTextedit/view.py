"""
view
===============================================================================
"""
from wbBase.document import dbg
from wbBase.document.view import View

from .window import TextWindow


class TextView(View):
    frameType = TextWindow

    def OnUpdate(self, sender, hint):
        result = False
        dbg(f"TextView.OnUpdate(sender={sender}, hint={hint})", indent=1)
        if hint:
            if hint[0] == "load" and sender == self.document:
                dbg("TextView.OnUpdate() load text into control")
                self.frame.SetText(self.document._data)
                result = True
            else:
                result = View.OnUpdate(self, sender, hint)
        dbg(f"TextView.OnUpdate() -> done, return {result}", indent=0)
        return result
