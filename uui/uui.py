from __future__ import annotations
from enum import IntEnum, auto, StrEnum
from typing import Callable, Any, Optional


Publisher = list


class WidgetTypes(StrEnum):
    NONE = ("NONE",)
    BUTTON = "BUTTON"


class Commands(StrEnum):
    NONE = "NONE"
    CREATE = "CREATE"
    SET_TEXT = "SET_TEXT"
    ONCLICK = "ONCLICK"


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
        self.numbers = map(lambda num: int(num), data["numbers"])
        self.strings = data["strings"]
        self.bools = map(lambda value: bool(value), data["bools"])


class Widget:
    def __init__(self) -> None:
        self.visible: bool = True
        self.enabled: bool = True
        self.text: str = ""
        self.type: WidgetTypes = WidgetTypes.NONE
        self.id = -1


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
    for message in messages:
        if message.command == Commands.ONCLICK:
            widget = widget_store.get(message.id)
            widget.onclick.func(widget, message, widget.onclick.param)

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


def default_func(Widget: Widget, message: Message, param: Any) -> None:
    print("Default Function")


DEFAULT_ACTION = create_action(default_func, None)


class ClickableWidget:
    def __init__(self) -> None:
        self.onclick: WidgetAction = default_func


class Button(Widget, ClickableWidget):
    pass


def send_create_widget(widget: Widget, publisher: Publisher):
    msg = Message()
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
    widget_store.add(button)

    send_create_widget(button, publisher)

    return button


def set_text(widget: Widget, text: str, publisher: Publisher):
    widget.text = text
    send_text(widget, publisher)


def set_onclick(widget: ClickableWidget, action: WidgetAction) -> None:
    widget.onclick = action
