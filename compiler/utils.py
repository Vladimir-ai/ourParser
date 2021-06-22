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
    XOR = '^'

    def __str__(self):
        return self.value


bin_map = {
    BinOp.ADD: 'add',
    BinOp.SUB: 'sub',
    BinOp.MUL: 'mul',
    BinOp.DIV: 'div',
    BinOp.GE: 'clt\n'
              'ldc.i4.0\n'
              'ceq',
    BinOp.LE: 'cgt\n'
              'idc.i4.0\n'
              'ceq',
    BinOp.NEQUALS: 'ceq'
                   'idc.i4.0\n'
                   'ceq',
    BinOp.EQUALS: 'ceq',
    BinOp.GT: 'cgt',
    BinOp.LT: 'clt',
    BinOp.BIT_AND: 'and',
    BinOp.BIT_OR: 'or',
    BinOp.XOR: 'xor',
    BinOp.LOGICAL_AND: 'and',
                       # 'idc.i4.0\n'
                       # 'ceq\n'
                       # 'idc.i4.0\n'
                       # 'ceq',
    BinOp.LOGICAL_OR: 'or'
                      # 'idc.i4.0\n'
                      # 'ceq\n'
                      # 'idc.i4.0\n'
                      # 'ceq'
}


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


def to_msil_type(type):
    result = str(type).replace('array char', 'char[]') \
        .replace('array float', 'float[]') \
        .replace('array bool', 'bool[]') \
        .replace('array int', 'int[]') \
        .replace("int", "int32") \
        .replace("float", "float32") \
        .replace("bool", "bool") \
        .replace("char", "char") \
        .replace("void", "void")


    return result

def to_msil_arr_ind_store_type(type):
    result = str(type).replace("int", "i4") \
        .replace("float", "r4") \
        .replace("bool", "i1") \
        .replace("char", "i2") \
        .replace("void", "???")

    return result

def to_msil_arr_ind_load_type(type):
    result = str(type).replace("int", "i4") \
        .replace("float", "r4") \
        .replace("bool", "u1") \
        .replace("char", "u2") \
        .replace("void", "???")
    return result

def to_msil_arr_type(type):
    result = str(type).replace("int", "Int32") \
        .replace("float", "Simple") \
        .replace("bool", "Boolean") \
        .replace("char", "Char") \
        .replace("void", "???")

    return result

def to_msil_inner_type(type):
    result = str(type).replace("int", "i4") \
        .replace("float", "r4") \
        .replace("bool", "bool") \
        .replace("char", "char") \
        .replace("void", "void")

    return result


def bin_to_msil(type: BinOp):
    return bin_map[type]

def to_msil_func(name: str) -> str:
    ret = ''
    if isBuiltinFunc(name):
        if name == 'print_float':
            ret += 'void [mscorlib]System.Console::WriteLine(float32)'
        elif name == 'print_int':
            ret += 'void [mscorlib]System.Console::WriteLine(int32)'
        elif name == 'print_char':
            ret += 'void [mscorlib]System.Console::WriteLine(char)'
        elif name == 'print_bool':
            ret += 'void [mscorlib]System.Console::WriteLine(bool)'
        elif name == 'print_string':
            ret += 'void [mscorlib]System.Console::WriteLine(char[])'
        elif name == 'read_float':
            ret += 'string [mscorlib]System.Console::ReadLine()\n' \
                   'call    float32 [mscorlib]System.Single::Parse(string)'
        elif name == 'read_int':
            ret += 'string [mscorlib]System.Console::ReadLine()\n' \
                   'call    int32 [mscorlib]System.Int32::Parse(string)'
        elif name == 'read_char':
            ret += 'string [mscorlib]System.Console::ReadLine()\n' \
                   'call    char [mscorlib]System.Char::Parse(string)'
        elif name == 'read_bool':
            ret += 'string [mscorlib]System.Console::ReadLine()\n' \
                   'call    bool [mscorlib]System.Boolean::Parse(string)'
        elif name == 'read_string':
            ret += 'string [mscorlib]System.Console::ReadLine()\n' \
                   'callvirt    instance char[] [mscorlib]System.String::ToCharArray()'
    else:
        ret = f'Program::{name}'
    return ret


def isBuiltinFunc(name: str) -> bool:
    if name == "print_float" \
            or name == "print_int" \
            or name == "print_char" \
            or name == "print_bool" \
            or name == "print_string" \
            or name == "read_int" \
            or name == "read_float" \
            or name == "read_bool" \
            or name == "read_string" \
            or name == "read_char":
        return True

    return False
