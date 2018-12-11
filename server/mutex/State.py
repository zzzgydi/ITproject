# -*- coding=utf-8 -*-


from enum import IntEnum

class State(IntEnum):
    OK          = 0
    DBErr       = 100
    PwdErr      = 101
    ActErr      = 102
