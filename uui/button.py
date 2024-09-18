from .widget import Widget
from .widgettype import WidgetType
from .clickablewidget import ClickableWidget
from .eventhandler import EventHandler
from .widgetaction import WidgetAction, Action, DEFAULT_ACTION
from .message import Message
from .widgetstore import WidgetStore
from .publisher import Publisher, send_create_widget

class Button(ClickableWidget):
    def __init__(self):
        super().__init__()

def create_button(widget_store: WidgetStore, publisher: Publisher) -> Widget:
    button = Button()
    button.type = WidgetType.BUTTON
    button.handle_event = button_event_handler
    button.onclick = DEFAULT_ACTION
    widget_store.add(button)

    send_create_widget(button, publisher)

    return button

def button_event_handler(widget: Widget, message: Message) -> None:
    if message.command == "ONCLICK":
        button: Button = widget
        if button.onclick and button.onclick.func:
            button.onclick.func(widget, message, button.onclick.param)