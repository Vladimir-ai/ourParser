from enum import Enum


class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    GE = '>='
    LE = '<='
    NEQUALS = '<>'
    EQUALS = '=='
    GT = '>'
    LT = '<'
    BIT_AND = '&'
    BIT_OR = '|'
    LOGICAL_AND = '&&'
    LOGICAL_OR = '||'

    def __str__(self):
        return self.value


class BaseType(Enum):
    VOID = 'void'
    INT = 'int'
    CHAR = 'char'
    FLOAT = 'float'
    BOOL = 'bool'

    def __str__(self):
        return self.value


class ArrayType(Enum):
    INT = 'int'
    CHAR = 'char'
    FLOAT = 'float'
    BOOL = 'bool'

    def __str__(self):
        return f"array {self.value}"


def getLLVMtype(type):
    result = str(type).replace("int", "i32") \
        .replace("float", "double") \
        .replace("bool", "i1") \
        .replace("char", "i8") \
        .replace("void", "void")

    return result


def getBinOp(binOp, type: BaseType):
    result = str(binOp).replace("+", "add") \
        .replace("-", "sub") \
        .replace("*", "mul").replace("/", "sdiv") \
        .replace(">=", "icmp sge").replace("<=", "icmp sle") \
        .replace("<>", "icmp ne").replace("==", "icmp eq") \
        .replace(">", "icmp sgt").replace("<", "icmp slt") \
        .replace("&", "and").replace("|", "or")

    if type == BaseType.FLOAT:
        result = str(binOp).replace("+", "fadd") \
            .replace("-", "fsub") \
            .replace("*", "fmul").replace("/", "fdiv") \
            .replace(">=", "fcmp oge").replace("<=", "fcmp ole") \
            .replace("<>", "fcmp one").replace("==", "fcmp oeq") \
            .replace(">", "fcmp ogt").replace("<", "fcmp olt") \
            .replace("&", "and").replace("|", "or")

    return result


def getConvOp(opFrom: BaseType, opTo: BaseType) -> str:
    if ((opFrom == BaseType.BOOL or opFrom == BaseType.CHAR) \
        and (opTo == BaseType.INT)) or (opFrom == BaseType.BOOL and opTo == BaseType.CHAR):
        return "zext"

    if (opFrom == BaseType.INT and (opTo == BaseType.BOOL or opTo == BaseType.CHAR)) \
            or (opFrom == BaseType.CHAR and opTo == BaseType.BOOL):
        return "trunc"

    if (opFrom == BaseType.FLOAT and (opTo == BaseType.BOOL or opTo == BaseType.INT)):
        return "fptoui"

    if (opFrom == BaseType.INT or opFrom == BaseType.BOOL) and opTo == BaseType.FLOAT:
        return "sitofp"
