from .publisher import Publisher
from .widgetstore import WidgetStore
from .message import Message, Commands
from typing import Optional, Any, Callable
from .publisher import Publisher
from .window import create_window, Window

class Application:
    def __init__(self) -> None:
        self.publisher: Publisher = Publisher()
        self.widgetStore: WidgetStore = WidgetStore()
        self.app_state: Optional[Any] = None

SetupFunction = Callable[[Application, list[Message]], Publisher]
LoopFunction = Callable[[Application, list[Message]], Publisher]

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

def standard_setup(app: Application) -> Window:
    return create_window(app.widgetStore, app.publisher)