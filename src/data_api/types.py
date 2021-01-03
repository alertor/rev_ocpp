from enum import Enum
from typing import Optional


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
