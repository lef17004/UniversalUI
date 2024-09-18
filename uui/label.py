from .framework import Widget
from .framework import WidgetType
from .framework import WidgetAction, DEFAULT_ACTION
from .framework import EventHandler
from .clickablewidget import ClickableWidget
from .framework import Message
from .framework import WidgetStore
from .framework import Publisher, send_create_widget_msg

class Label(Widget):...


def create_label(widget_store: WidgetStore, publisher: Publisher, text: str) -> Widget:
    label = Label()
    label.type = WidgetType.LABEL
    widget_store.add(label)

    msg = Message()
    msg.strings[0] = text
    send_create_widget_msg(label, publisher, msg)

    return label