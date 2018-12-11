# -*- coding=utf-8 -*-

from enum import IntEnum

class State(IntEnum):
    OK          = 0
    DBErr       = 100
    PwdErr      = 101
    ActErr      = 102
    RegErr      = 103
    FormErr     = 300
    Error       = 400
    NotLogin    = 401
