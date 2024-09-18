from __future__ import annotations
from enum import IntEnum, auto, Enum, StrEnum
from typing import Callable, Any, Optional
from .message import WidgetTypes, Commands, Message
from .widget import Widget
from .window import Window
from .widgetstore import WidgetStore
from .publisher import Publisher, send_create_widget
from .application import Application, LoopFunction, SetupFunction
from .widgetaction import Action, WidgetAction, create_action, DEFAULT_ACTION
from .eventhandler import EventHandler
from .button import Button
Publisher = list


def handle_events(
    messages: list[Message], widget_store: WidgetStore, publisher: Publisher
) -> list[Message]:
    print("Handle event")
    for message in messages:
        print(message.to_dict())
        if message.command == Commands.ONCLICK or message.command == Commands.CHAR_TYPED:
            print("Event")
            widget = widget_store.get(message.id)
            widget.handle_event(widget, message)

    return []






def textbox_event_handler(widget: Widget, message: Message) -> None:
    if message.command == "CHAR_TYPED":
        if widget.on_char_typed and widget.on_char_typed.func:
            widget.on_char_typed.func(widget, message, widget.on_char_typed.param)


def default_textbox_action(widget: Widget, message: Message, param: Any):
    widget.text = message.strings[0]
    print(f"New Text: {widget.text}")

def checkbox_handle_event(widget: Widget, message: Message):
    print("Checkboxx")
    print(message.bools[0])
    widget.is_checked = message.bools[0]
    onclick_action = widget.onclick
    if onclick_action and onclick_action.func:
        onclick_action.func(widget, message, onclick_action.param)

DEFAULT_TEXT_INPUT_FUNC = create_action(default_textbox_action, None)

class TextBox(Widget):
    def __init__(self):
        self.handle_event: Optional[EventHandler] = None
        self.on_char_typed: Optional[WidgetAction] = None

class CheckBox(Widget):
    def __init__(self):
        self.is_checked: bool = False
        self.onclick: WidgetAction = None
        self.handle_event: EventHandler = None

class Group(Widget):
    def __init__(self):
        self.widgets = [None] * 10
        self.capacity = 0
        self.size = 0
        

class Label(Widget):...



def send_create_widget_msg(widget: Widget, publisher: Publisher, msg: Message):
    msg.command = Commands.CREATE
    msg.type = widget.type
    msg.id = widget.id

    publisher.add(msg)


def send_text(widget: Widget, publisher: Publisher):
    msg = Message()
    msg.command = Commands.SET_TEXT
    msg.type = widget.type
    msg.id = widget.id
    msg.strings[0] = widget.text

    publisher.add(msg)


def create_label(widget_store: WidgetStore, publisher: Publisher, text: str) -> Widget:
    label = Label()
    label.type = WidgetTypes.LABEL
    widget_store.add(label)

    msg = Message()
    msg.strings[0] = text
    send_create_widget_msg(label, publisher, msg)

    return label

def create_checkbox(widget_store: WidgetStore, publisher: Publisher) -> Widget:
    checkbox = CheckBox()
    checkbox.type = WidgetTypes.CHECKBOX
    checkbox.handle_event = checkbox_handle_event
    checkbox.onclick = DEFAULT_ACTION
    widget_store.add(checkbox)

    send_create_widget(checkbox, publisher)

    return checkbox

def create_window(widget_store: WidgetStore, publisher: Publisher) -> Widget:
    window = Window()
    window.type = WidgetTypes.WINDOW
    widget_store.add(window)

    send_create_widget(window, publisher)

    return window

def create_textbox(widget_store: WidgetStore, publisher: Publisher) -> Window:
    textbox = TextBox()
    textbox.type = WidgetTypes.TEXTBOX
    textbox.handle_event = textbox_event_handler
    textbox.on_char_typed = DEFAULT_TEXT_INPUT_FUNC
    widget_store.add(textbox)

    send_create_widget(textbox, publisher)

    return textbox

def create_group(widget_store: WidgetStore, publisher: Publisher) -> None:
    group = Group()
    group.type = WidgetTypes.GROUP
    group.capacity = 10
    group.size = 0
    widget_store.add(group)

    send_create_widget(group)

    return group

def set_text(widget: Widget, text: str, publisher: Publisher):
    widget.text = text
    send_text(widget, publisher)


def set_onclick(widget: ClickableWidget, action: WidgetAction) -> None:
    widget.onclick = action


def standard_setup(app: Application) -> Window:
    return create_window(app.widgetStore, app.publisher)

class SnapPoint(StrEnum):
    TOP_LEFT = "TOP_LEFT"
    TOP_CENTER = "TOP_CENTER"
    TOP_RIGHT = "TOP_RIGHT"
    CENTER_LEFT = "CENTER_LEFT"
    CENTER = "CENTER"
    CENTER_RIGHT = "CENTER_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_CENTER = "BOTTOM_CENTER"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"


def snap_to_widget(
    publisher: Publisher,
    widget1: Widget,
    widget2: Widget,
    point1: SnapPoint,
    point2: SnapPoint,
    x_offset: float,
    y_offset: float,
) -> None:
    msg = Message()
    msg.command = Commands.SNAP
    msg.id = widget1.id
    msg.numbers[0] = widget2.id
    msg.strings[0] = point1
    msg.strings[1] = point2
    msg.numbers[1] = x_offset
    msg.numbers[2] = y_offset

    publisher.add(msg)

def add_to_group(group: Group, widget: Widget):
    if group.size < group.capacity:
        # Add code to remove existing parent
        widget.parent = group
        group.widgets[group.size] = widget
        group.size += 1

        message = Message()
        message.command = Commands.ADD_TO_GROUP
        message.id = group.id
        message.numbers[0] = widget.id

