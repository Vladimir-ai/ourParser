from enum import Enum


class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MULT = '*'
    DIV = '/'
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    EQUAL = '=='
    NOT_EQUAL = '!='
    AND = '&&'
    OR = '||'
