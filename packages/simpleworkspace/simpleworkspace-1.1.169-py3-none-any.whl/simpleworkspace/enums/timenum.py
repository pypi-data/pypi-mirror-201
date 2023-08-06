from enum import Enum as _Enum

class TimeEnum(_Enum):
    Second = 1
    Minute = 60
    Hour = Minute * 60
    Day = 24 * Hour