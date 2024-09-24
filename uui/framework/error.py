from enum import IntEnum, auto

class Error(IntEnum):
    NO_ERROR = auto()
    OUT_OF_BOUNDS = auto()
    ALREADY_IN_GROUP = auto()