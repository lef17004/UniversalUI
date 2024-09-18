from .widget import Widget
from .widgettype import WidgetType
from .widgetaction import WidgetAction, DEFAULT_ACTION
from .eventhandler import EventHandler
from .clickablewidget import ClickableWidget
from .message import Message
from .widgetstore import WidgetStore
from .publisher import Publisher, send_create_widget_msg

class Label(Widget):...


def create_label(widget_store: WidgetStore, publisher: Publisher, text: str) -> Widget:
    label = Label()
    label.type = WidgetType.LABEL
    widget_store.add(label)

    msg = Message()
    msg.strings[0] = text
    send_create_widget_msg(label, publisher, msg)

    return label