from __future__ import annotations
from enum import StrEnum

class WidgetTypes(StrEnum):
    NONE = "NONE"
    BUTTON = "BUTTON"
    WINDOW = "WINDOW"
    LABEL = "LABEL"
    TEXTBOX = "TEXTBOX"
    CHECKBOX = "CHECKBOX"
    GROUP = "GROUP"



class Widget:
    def __init__(self) -> None:
        self.visible: bool = True
        self.enabled: bool = True
        self.text: str = ""
        self.type: WidgetTypes = WidgetTypes.NONE
        self.id = -1
        self.parent: Optional[Widget] = None