from enum import Enum


class EqualizationStandard(Enum):
    IEC = "IEC"
    CCIR = "IEC1"
    NAB = "IEC2"


class SpeedStandard(Enum):
    I = 0.9375
    II = 1.875
    III = 3.75
    IV = 7.5
    V = 15
    VI = 30
