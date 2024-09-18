from .message import Message
from .widget import Widget
from typing import Any, Callable

Action = Callable[[Widget, Message, Any], None]

class WidgetAction:
    def __init__(self):
        self.func: Optional[Action] = None
        self.param: Optional[Any] = None

def create_action(func: Action, param: Any) -> WidgetAction:
    action = WidgetAction()
    action.func = func
    action.param = param
    return action

def default_func(Widget: Widget, message: Message, param: Any) -> None:
    print("Default Function")

DEFAULT_ACTION: WidgetAction = create_action(default_func, None)