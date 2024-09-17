from uui import (
    start_app,
    Message,
    Commands,
    WidgetTypes,
    Application,
    create_button,
    set_text,
    Publisher,
    Widget,
    set_onclick,
    WidgetAction,
    handle_events,
    create_action,
    standard_setup,
    SnapPoint,
    snap_to_widget,
    create_label,
    create_textbox,
    create_checkbox
)
from typing import Any

app = Application()


def setup(application: Application, messages: list[Message]) -> Publisher:
    window = standard_setup(application)
    publisher = application.publisher
    widget_store = application.widgetStore

    button = create_button(widget_store, publisher)
    set_text(button, "Button", publisher)

    button2 = create_button(widget_store, publisher)
    set_text(button2, "Button2", publisher)

    button3 = create_button(widget_store, publisher)
    set_text(button3, "Button3", publisher)

    button_action = create_action(on_button_press, "Tacos")

    set_onclick(button, button_action)

    snap_to_widget(publisher, button2, window, SnapPoint.CENTER, SnapPoint.CENTER, 0, 0)
    snap_to_widget(publisher, button, button2, SnapPoint.BOTTOM_CENTER, SnapPoint.TOP_CENTER, 0, 0)
    snap_to_widget(publisher, button3, button2, SnapPoint.TOP_CENTER, SnapPoint.BOTTOM_CENTER, 0, 0)

    label = create_label(widget_store, publisher, "My Label Text")

    snap_to_widget(publisher, label, button2, SnapPoint.CENTER_RIGHT, SnapPoint.CENTER_LEFT, 0, 0)

    textbox = create_textbox(widget_store, publisher)

    checkbox = create_checkbox(widget_store, publisher)

    return publisher


def loop(application: Application, messages: list[Message]) -> Publisher:
    publisher = application.publisher
    widget_store = application.widgetStore

    unused_events = handle_events(messages, widget_store, publisher)

    return publisher


def on_button_press(widget: Widget, message: Message, param: Any) -> None:
    print("Button is pressed with parameter: " + str(param))


start_app(setup, loop, app)
