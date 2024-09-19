from typing import Optional

from .framework import Widget
from .framework import WidgetType
from .framework import WidgetAction, DEFAULT_ACTION
from .framework import EventHandler
from .clickablewidget import ClickableWidget
from .framework import Message
from .framework import WidgetStore
from .framework import Publisher, send_create_widget

import framework

class Group(Widget):
    def __init__(self):
        self.widgets: list[Optional[Widget]] = [None] * 10
        self.capacity: int = 0
        self.size: int = 0

def create_group(widget_store: WidgetStore, publisher: Publisher) -> None:
    group = Group()
    group.type = WidgetType.GROUP
    group.capacity = 10
    group.size = 0
    widget_store.add(group)

    send_create_widget(group)

    return group


def add_to_group(group: Group, widget: Widget, publisher: Publisher):
    if widget.parent == group:
        return

    if group.size < group.capacity:
        # Add code to remove existing parent
        if widget.parent:
            remove_from_group(widget.parent, widget, publisher)

        widget.parent = group
        group.widgets[group.size] = widget
        group.size += 1

        message = Message()
        message.command = Commands.ADD_TO_GROUP
        message.id = group.id
        message.numbers[0] = widget.id

def remove_from_group(group: Group, widget: Widget, publisher: Publisher):
    for child in group.widgets:
        if child == widget:
            group.widgets.remove(widget)
            widget.parent = None

            msg = Message()
            msg.command = framework.Commands.REMOVE_FROM_GROUP
            msg.id = group.id
            msg.numbers[0] = widget.id
            publisher.add(msg) 
