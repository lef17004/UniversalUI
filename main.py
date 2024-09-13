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
    create_action
)
from typing import Any

app = Application()


def setup(application: Application, messages: list[Message]) -> Publisher:
    publisher = application.publisher
    widget_store = application.widgetStore

    button = create_button(widget_store, publisher)
    set_text(button, "Michael's Amazing Button", publisher)

    button_action = create_action(on_button_press, "Tacos")

    set_onclick(button, button_action)

    return publisher


def loop(application: Application, messages: list[Message]) -> Publisher:
    publisher = application.publisher
    widget_store = application.widgetStore

    unused_events = handle_events(messages, widget_store, publisher)

    return publisher


def on_button_press(widget: Widget, message: Message, param: Any) -> None:
    print("Button is pressed with parameter: " + str(param))


start_app(setup, loop, app)
