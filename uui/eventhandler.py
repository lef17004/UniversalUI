from typing import Callable, Any
from .widget import Widget
from .message import Message

EventHandler = Callable[[Widget, Message], None]


