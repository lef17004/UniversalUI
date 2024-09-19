from .clickablewidget import ClickableWidget
import uui.framework as fw

class Button(ClickableWidget):
    def __init__(self):
        super().__init__()

def create_button(widget_store: fw.WidgetStore, publisher: fw.Publisher) -> fw.Widget:
    button = Button()
    button.type = fw.WidgetType.BUTTON
    button.handle_event = button_event_handler
    button.onclick = fw.DEFAULT_ACTION
    widget_store.add(button)

    fw.send_create_widget(button, publisher)

    return button

def button_event_handler(widget: fw.Widget, message: fw.Message) -> None:
    if message.command == "ONCLICK":
        button: Button = widget
        if button.onclick and button.onclick.func:
            button.onclick.func(widget, message, button.onclick.param)