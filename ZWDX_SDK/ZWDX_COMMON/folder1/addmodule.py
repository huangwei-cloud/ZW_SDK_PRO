from enum import Enum


class ZW_STATUS(Enum):
    DISABLE = 0
    ENABLE = 1
    OPEN = 2
    CLOSE = 3
    SUCCESS = 4
    FAIL = 5


class ZW_CH(Enum):
    CH1 = 0x0001
    CH2 = 0x0002
    CH3 = 0x0004
    CH4 = 0x0008
    CH5 = 0x0010
    CH6 = 0x0020
    CH7 = 0x0040
    CH8 = 0x0080
    CHALL = 0x00FF


def add(x, y):
    return x + y
