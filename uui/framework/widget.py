from __future__ import annotations
from enum import StrEnum
from .message import Message, Commands, WidgetType

class Widget:
    def __init__(self) -> None:
        self.visible: bool = True
        self.enabled: bool = True
        self.text: str = ""
        self.type: WidgetType = WidgetType.NONE
        self.id = -1
        self.parent: Optional[Widget] = None

def send_text(widget: Widget, publisher: Publisher):
    msg = Message()
    msg.command = Commands.SET_TEXT
    msg.type = widget.type
    msg.id = widget.id
    msg.strings[0] = widget.text

    publisher.add(msg)


def set_text(widget: Widget, text: str, publisher: Publisher):
    widget.text = text
    send_text(widget, publisher)
