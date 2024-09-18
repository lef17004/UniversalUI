from .framework import Widget
from .framework import WidgetType
from .framework import WidgetAction, DEFAULT_ACTION
from .framework import EventHandler
from .clickablewidget import ClickableWidget
from .framework import Message
from .framework import WidgetStore
from .framework import Publisher, send_create_widget

class CheckBox(ClickableWidget):
    def __init__(self):
        super().__init__()
        self.is_checked: bool = False

def create_checkbox(widget_store: WidgetStore, publisher: Publisher) -> Widget:
    checkbox = CheckBox()
    checkbox.type = WidgetType.CHECKBOX
    checkbox.handle_event = checkbox_handle_event
    checkbox.onclick = DEFAULT_ACTION
    widget_store.add(checkbox)

    send_create_widget(checkbox, publisher)

    return checkbox

def checkbox_handle_event(widget: Widget, message: Message):
    print("Checkboxx")
    print(message.bools[0])
    widget.is_checked = message.bools[0]
    onclick_action = widget.onclick
    if onclick_action and onclick_action.func:
        onclick_action.func(widget, message, onclick_action.param)
