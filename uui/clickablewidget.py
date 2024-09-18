from .widget import Widget
from .widgetaction import DEFAULT_ACTION, Action, WidgetAction
from .eventhandler import EventHandler


class ClickableWidget(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.handle_event: Optional[EventHandler] = None
        self.onclick: Optional[WidgetAction] = None