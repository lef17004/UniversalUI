from .widget import Widget
from .widgettype import WidgetType
from .widgetstore import WidgetStore
from .publisher import Publisher, send_create_widget

class Window(Widget): pass

def create_window(widget_store: WidgetStore, publisher: Publisher) -> Widget:
    window = Window()
    window.type = WidgetType.WINDOW
    widget_store.add(window)

    send_create_widget(window, publisher)

    return window