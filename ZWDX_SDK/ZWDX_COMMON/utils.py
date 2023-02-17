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
    # CH9 = 0x0100
    # CH10 = 0x0200
    # CH11 = 0x0400
    # CH12 = 0x0800
    # CH13 = 0x1000
    # CH14 = 0x2000
    # CH15 = 0x4000
    # CH16 = 0x8000
    CHALL = 0x00FF

