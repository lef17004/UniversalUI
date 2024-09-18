from .publisher import Publisher
from .widgetstore import WidgetStore
from .message import Message
from typing import Optional, Any, Callable

class Application:
    def __init__(self) -> None:
        self.publisher: Publisher = Publisher()
        self.widgetStore: WidgetStore = WidgetStore()
        self.app_state: Optional[Any] = None

SetupFunction = Callable[[Application, list[Message]], Publisher]
LoopFunction = Callable[[Application, list[Message]], Publisher]