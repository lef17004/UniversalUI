from __future__ import annotations
from enum import IntEnum, auto, Enum
from typing import Callable, Any, Optional


Publisher = list
class StrEnum(str, Enum):
	...

class WidgetTypes(StrEnum):
    NONE = "NONE"
    BUTTON = "BUTTON"
    WINDOW = "WINDOW"
    LABEL = "LABEL"
    TEXTBOX = "TEXTBOX"
    CHECKBOX = "CHECKBOX"


class Commands(StrEnum):
    NONE = "NONE"
    CREATE = "CREATE"
    SET_TEXT = "SET_TEXT"
    ONCLICK = "ONCLICK"
    SNAP = "SNAP"
    CHAR_TYPED = "CHAR_TYPED"


class Message:
    def __init__(self) -> None:
        self.command = Commands.NONE
        self.id = -1
        self.type: WidgetTypes = WidgetTypes.NONE
        self.numbers = [0, 0, 0, 0, 0]
        self.strings = ["", "", "", "", ""]
        self.bools = [False, False, False, False, False]

    def to_dict(self) -> dict:
        return {
            "command": self.command,
            "id": self.id,
            "widgetType": self.type,
            "numbers": self.numbers,
            "strings": self.strings,
            "bools": self.bools,
        }

    def from_dict(self, data: dict):
        self.command = data["command"]
        self.id = int(data["id"])
        self.type = data["widgetType"]
        self.numbers = list(map(lambda num: int(num), data["numbers"]))
        self.strings = data["strings"]
        self.bools = list(map(lambda value: bool(value), data["bools"]))


class Widget:
    def __init__(self) -> None:
        self.visible: bool = True
        self.enabled: bool = True
        self.text: str = ""
        self.type: WidgetTypes = WidgetTypes.NONE
        self.id = -1

class Window(Widget): pass


class WidgetStore:
    def __init__(self):
        self._id_counter = 0
        self._widgets = []

    def add(self, widget: Widget):
        widget.id = self._id_counter
        self._id_counter += 1
        self._widgets.append(widget)

    def get(self, id: int):
        return self._widgets[id]


class Publisher:
    def __init__(self):
        self._messages: list[Message] = []

    def add(self, message: Message):
        self._messages.append(message)

    def clear(self):
        self._messages.clear()

    def checkout_as_json(self) -> list[dict]:
        json = list(map(lambda message: message.to_dict(), self._messages))
        self.clear()
        return json


class Application:
    def __init__(self) -> None:
        self.publisher: Publisher = Publisher()
        self.widgetStore: WidgetStore = WidgetStore()
        self.app_state: Optional[Any] = None




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


Action = Callable[[Widget, Message, Any], None]


class WidgetAction:
    def __init__(self):
        self.func: Optional[Action] = None
        self.param: Optional[Any] = None


def create_action(func: Action, param: Any):
    action = WidgetAction()
    action.func = func
    action.param = param
    return action


SetupFunction = Callable[[Application, list[Message]], Publisher]
LoopFunction = Callable[[Application, list[Message]], Publisher]
EventHandler = Callable[[Widget, Message], None]

def default_func(Widget: Widget, message: Message, param: Any) -> None:
    print("Default Function")


DEFAULT_ACTION = create_action(default_func, None)


class ClickableWidget:
    def __init__(self) -> None:
        self.onclick: WidgetAction = DEFAULT_ACTION

def button_event_handler(widget: Widget, message: Message) -> None:
    if message.command == "ONCLICK":
        if widget.onclick and widget.onclick.func:
            widget.onclick.func(widget, message, widget.onclick.param)

def textbox_event_handler(widget: Widget, message: Message) -> None:
    if message.command == "CHAR_TYPED":
        if widget.on_char_typed and widget.on_char_typed.func:
            widget.on_char_typed.func(widget, message, widget.on_char_typed.param)

class Button(Widget):
    def __init__(self):
        super().__init__()
        self.handle_event: Optional[EventHandler] = None
        self.onclick: Optional[Action] = None

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
        self.widgets = [None * 10]
        

class Label(Widget):...

def send_create_widget(widget: Widget, publisher: Publisher):
    msg = Message()
    msg.command = Commands.CREATE
    msg.type = widget.type
    msg.id = widget.id

    publisher.add(msg)

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


def create_button(widget_store: WidgetStore, publisher: Publisher) -> Widget:
    button = Button()
    button.type = WidgetTypes.BUTTON
    button.handle_event = button_event_handler
    button.onclick = DEFAULT_ACTION
    widget_store.add(button)

    send_create_widget(button, publisher)

    return button

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
