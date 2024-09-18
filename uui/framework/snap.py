from enum import StrEnum
from .publisher import Publisher
from .widget import Widget
from .widget import WidgetType
from .message import Message, Commands

class SnapPoint(StrEnum):
    TOP_LEFT = "TOP_LEFT"
    TOP_CENTER = "TOP_CENTER"
    TOP_RIGHT = "TOP_RIGHT"
    CENTER_LEFT = "CENTER_LEFT"
    CENTER = "CENTER"
    CENTER_RIGHT = "CENTER_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_CENTER = "BOTTOM_CENTER"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"


def snap_to_widget(
    publisher: Publisher,
    widget1: Widget,
    widget2: Widget,
    point1: SnapPoint,
    point2: SnapPoint,
    x_offset: float,
    y_offset: float,
) -> None:
    msg = Message()
    msg.command = Commands.SNAP
    msg.id = widget1.id
    msg.numbers[0] = widget2.id
    msg.strings[0] = point1
    msg.strings[1] = point2
    msg.numbers[1] = x_offset
    msg.numbers[2] = y_offset

    publisher.add(msg)