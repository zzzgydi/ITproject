# -*- coding=utf-8 -*-

from enum import IntEnum

class State(IntEnum):
    OK          = 0
    DBErr       = 100
    PwdErr      = 101
    ActErr      = 102
    RegErr      = 103
    ListNone    = 104
    NoSale      = 105
    FormErr     = 300
    BookNExit   = 304
    Error       = 400
    NotLogin    = 401
    NoBookErr   = 201
    NoOrderErr  = 202
    OUErr       = 203
    Debug       = 500
    
