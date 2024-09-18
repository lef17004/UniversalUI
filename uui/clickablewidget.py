from .framework import Widget, EventHandler, DEFAULT_ACTION, Action, WidgetAction

class ClickableWidget(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.handle_event: Optional[EventHandler] = None
        self.onclick: Optional[WidgetAction] = None

def set_onclick(widget: ClickableWidget, action: WidgetAction) -> None:
    widget.onclick = action