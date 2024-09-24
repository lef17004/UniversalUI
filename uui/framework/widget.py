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
        self.next: Optional[Widget] = None
        self.prev: Optional[Widget] = None

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

def set_next(root_widget: Widget, new_widget: Widget):
    if root_widget.next:
        set_next(root_widget.next, new_widget)
    else:
        root_widget.next = new_widget
        new_widget.prev = root_widget


def remove_widget_from_list(root: Widget, current: Widget, target: Widget) -> Widget:

    if current is None:
        return root, False

    if root == target:
        if root.next:
            root.next.prev = None
        return root.next, False

    if current == target:
        prev_widget: Widget = current.prev
        next_widget: Widget = current.next
        if prev_widget:
            prev_widget.next = next_widget
        if next_widget:
            next_widget.prev = prev_widget

        return root, True

    return remove_widget_from_list(root, current.next, target)

def remove_index_from_list(root: Widget, current: Widget, current_index: int, target_index: int):
    if current is None:
        return root, False

    if target_index == 0:
        if root.next:
            root.next.prev = None
        return root.next, False

    if current_index == target_index:
        prev_widget: Widget = current.prev
        next_widget: Widget = current.next
        if prev_widget:
            prev_widget.next = next_widget
        if next_widget:
            next_widget.prev = prev_widget

        return root, True

    return remove_index_from_list(root, current.next, current_index + 1, target_index)
    