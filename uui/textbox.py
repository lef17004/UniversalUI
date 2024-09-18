from typing import Any
from .widget import Widget
from .widgettype import WidgetType
from .eventhandler import EventHandler
from.widgetaction import WidgetAction, create_action
from .message import Message
from .publisher import Publisher, send_create_widget
from .widgetstore import WidgetStore


class TextBox(Widget):
    def __init__(self):
        self.handle_event: Optional[EventHandler] = None
        self.on_char_typed: Optional[WidgetAction] = None

def create_textbox(widget_store: WidgetStore, publisher: Publisher) -> TextBox:
    textbox = TextBox()
    textbox.type = WidgetType.TEXTBOX
    textbox.handle_event = textbox_event_handler
    textbox.on_char_typed = DEFAULT_TEXT_INPUT_FUNC
    widget_store.add(textbox)

    send_create_widget(textbox, publisher)

    return textbox

def textbox_event_handler(widget: Widget, message: Message) -> None:
    if message.command == "CHAR_TYPED":
        if widget.on_char_typed and widget.on_char_typed.func:
            widget.on_char_typed.func(widget, message, widget.on_char_typed.param)

def default_textbox_action(widget: Widget, message: Message, param: Any):
    widget.text = message.strings[0]
    print(f"New Text: {widget.text}")

DEFAULT_TEXT_INPUT_FUNC = create_action(default_textbox_action, None)