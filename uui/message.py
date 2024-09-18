from enum import StrEnum
from .widget import WidgetTypes

class Commands(StrEnum):
    NONE = "NONE"
    CREATE = "CREATE"
    SET_TEXT = "SET_TEXT"
    ONCLICK = "ONCLICK"
    SNAP = "SNAP"
    CHAR_TYPED = "CHAR_TYPED"
    ADD_TO_GROUP = "ADD_TO_GROUP"

class Message:
    def __init__(self) -> None:
        self.command = Commands.NONE
        self.id = -1
        self.type: WidgetTypes = WidgetTypes.NONE
        self.numbers = [0, 0, 0, 0, 0]
        self.strings = ["", "", "", "", ""]
        self.bools = [False, False, False, False, False]

    def to_dict(self) -> dict:
        return {
            "command": self.command,
            "id": self.id,
            "widgetType": self.type,
            "numbers": self.numbers,
            "strings": self.strings,
            "bools": self.bools,
        }

    def from_dict(self, data: dict):
        self.command = data["command"]
        self.id = int(data["id"])
        self.type = data["widgetType"]
        self.numbers = list(map(lambda num: int(num), data["numbers"]))
        self.strings = data["strings"]
        self.bools = list(map(lambda value: bool(value), data["bools"]))