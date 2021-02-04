from enum import Enum
from typing import Optional

"""
This is the start of work around generic operators to access any data
Not currently functional
"""


class Operators(str, Enum):

    LessThan = 'lt'
    LessThanEquals = 'lte'
    Equals = 'eq'
    GreaterThanEquals = 'gte'
    GreaterThan = 'gt'
    NotEquals = 'ne'


class OperatorParameter(object):

    __slots__ = ['value', 'op']

    def __init__(self, value, op: Optional[Operators] = None):
        self.value = value
        self.op = op


class BucketType(str, Enum):
    Seconds = 'seconds'
    Minutes = 'minutes'
    Hours = 'hours'
    Days = 'days'
    Weeks = 'weeks'
    Months = 'months'
    Years = 'years'
