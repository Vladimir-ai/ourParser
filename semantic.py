from enum import Enum


class BaseType(Enum):
    VOID = 'void'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'

    def __str__(self):
        return self.value
