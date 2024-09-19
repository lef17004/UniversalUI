import uui
from typing import Any

app = uui.Application()


def setup(application: uui.Application, messages: list[uui.Message]) -> uui.Publisher:
    window = uui.standard_setup(application)
    publisher = application.publisher
    widget_store = application.widgetStore

    button = uui.create_button(widget_store, publisher)
    uui.set_text(button, "Button", publisher)

    button2 = uui.create_button(widget_store, publisher)
    uui.set_text(button2, "Button2", publisher)

    button3 = uui.create_button(widget_store, publisher)
    uui.set_text(button3, "Button3", publisher)

    button_action = uui.create_action(on_button_press, "Tacos")

    uui.set_onclick(button, button_action)

    uui.snap_to_widget(publisher, button2, window, uui.SnapPoint.CENTER, uui.SnapPoint.CENTER, 0, 0)
    uui.snap_to_widget(publisher, button, button2, uui.SnapPoint.BOTTOM_CENTER, uui.SnapPoint.TOP_CENTER, 0, 0)
    uui.snap_to_widget(publisher, button3, button2, uui.SnapPoint.TOP_CENTER, uui.SnapPoint.BOTTOM_CENTER, 0, 0)

    label = uui.create_label(widget_store, publisher, "My Label Text")

    uui.snap_to_widget(publisher, label, button2, uui.SnapPoint.CENTER_RIGHT, uui.SnapPoint.CENTER_LEFT, 0, 0)

    textbox = uui.create_textbox(widget_store, publisher)

    checkbox = uui.create_checkbox(widget_store, publisher)

    return publisher


def loop(application: uui.Application, messages: list[uui.Message]) -> uui.Publisher:
    publisher = application.publisher
    widget_store = application.widgetStore

    unused_events = uui.handle_events(messages, widget_store, publisher)

    return publisher


def on_button_press(widget: uui.Widget, message: uui.Message, param: Any) -> None:
    print("Button is pressed with parameter: " + str(param))


uui.start_app(setup, loop, app)
