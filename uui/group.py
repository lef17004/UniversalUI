from typing import Optional

from .framework import Widget, Error
from .framework import WidgetType
from .framework import WidgetAction, DEFAULT_ACTION
from .framework import EventHandler
from .clickablewidget import ClickableWidget
from .framework import Message
from .framework import WidgetStore
from .framework import Publisher, send_create_widget

import framework as fw

class Group(Widget):
    def __init__(self):
        self.size: int = 0
        self.child: Optional[Widget] = None

def create_group(widget_store: WidgetStore, publisher: Publisher) -> None:
    group = Group()
    group.type = WidgetType.GROUP
    group.size = 0
    group.child = None
    widget_store.add(group)

    send_create_widget(group)

    return group


def add_to_group(group: Group, widget: Widget, publisher: Publisher) -> Error:
    if widget.parent == group:
        return Error.ALREADY_IN_GROUP

    
    # Add code to remove existing parent
    if widget.parent:
        remove_from_group(widget.parent, widget, publisher)

    if group.child:
        fw.set_next(group.child, widget)
    else:
        group.child = widget

    widget += 1
    

    message = Message()
    message.command = Commands.ADD_TO_GROUP
    message.id = group.id
    message.numbers[0] = widget.id

def remove_widget_from_group(group: Group, widget: Widget, publisher: Publisher):
    group.child, did_remove = fw.remove_widget_from_list(group.child, group.child, widget)

    if did_remove:
        group.size -= 1
        widget.parent = group
        msg = Message()
        msg.command = framework.Commands.REMOVE_FROM_GROUP
        msg.id = group.id
        msg.numbers[0] = widget.id
        publisher.add(msg)

def remove_index_from_group(group: Group, index: Widget, publisher: Publisher):
    group.child, did_remove = fw.remove_index_from_list(group.child, group.child, 0, index)

    if did_remove:
        group.size -= 1
        widget.parent = group
        msg = Message()
        msg.command = framework.Commands.REMOVE_FROM_GROUP
        msg.id = group.id
        msg.numbers[0] = widget.id
        publisher.add(msg)


