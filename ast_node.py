from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum

from lark import Token

class KeyWords(Enum):
    RETURN = 'return'
    FOR = 'for'
    INT = 'int'
    CHAR = 'char'
    VOID = 'void'
    DOUBLE = 'double'
    FLOAT = 'float'

def checkNameAndException(name : str, text : str):
    if name.upper() in KeyWords.__dict__:
        raise BaseException("Using keyword in name of " + text)

class AstNode(ABC):
    def __init__(self, row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__()
        self.row = row
        self.line = line
        for k, v in props.items():
            setattr(self, k, v)

    @property
    def children(self) -> Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> [str, ...]:
        res = [str(self)]
        children_temp = self.children
        for i, child in enumerate(children_temp):
            ch0, ch = '├', '│'
            if i == len(children_temp) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None]) -> None:
        func(self)
        map(func, self.children)

    def __getitem__(self, index):
        return self.children[index] if index < len(self.children) else None


class ExprNode(AstNode):
    pass


class LiteralNode(ExprNode):
    def __init__(self, literal: str,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.literal = literal
        self.value = eval(literal)

    def __str__(self) -> str:
        return '{0} ({1})'.format(self.literal, type(self.value).__name__)


class IdentNode(ExprNode):
    def __init__(self, name: str,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.name = str(name)


    def __str__(self) -> str:
        return str(self.name)


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


class BinOpNode(ExprNode):
    def __init__(self, op: BinOp, arg1: ExprNode, arg2: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def children(self) -> Tuple[ExprNode, ExprNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.op.value)


class StmtNode(ExprNode):
    pass


class VarsDeclNode(StmtNode):
    def __init__(self, vars_type: StmtNode, *vars_list: Tuple[AstNode, ...],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        for var in vars_list:
            checkNameAndException(str(var), "var")
        self.vars_type = vars_type
        self.vars_list = vars_list

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.vars_type,) + self.vars_list

    def __str__(self) -> str:
        return 'var'


class CallNode(StmtNode):
    def __init__(self, func: IdentNode, *params: Tuple[ExprNode],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        checkNameAndException(str(func), "function")
        self.func = func
        self.params = params

    @property
    def children(self) -> Tuple[IdentNode, ...]:
        # return self.func, (*self.params)
        return (self.func,) + self.params

    def __str__(self) -> str:
        return 'call'


class AssignNode(StmtNode):
    def __init__(self, var: IdentNode, val: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        checkNameAndException(str(var), "var")
        self.var = var
        self.val = val

    @property
    def children(self) -> Tuple[IdentNode, ExprNode]:
        return self.var, self.val

    def __str__(self) -> str:
        return '='


class IfNode(StmtNode):
    def __init__(self, cond: ExprNode, then_stmt: StmtNode, else_stmt: Optional[StmtNode] = None,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.cond = cond
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    @property
    def children(self) -> Tuple[ExprNode, StmtNode, Optional[StmtNode]]:
        return (self.cond, self.then_stmt) + ((self.else_stmt,) if self.else_stmt else tuple())

    def __str__(self) -> str:
        return 'if'


class ForNode(AstNode):
    def __init__(self, init: Union[StmtNode, None], cond: Union[ExprNode, StmtNode, None],
                 step: Union[StmtNode, None], body: Union[StmtNode, None] = None,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.init = init if init else _empty
        self.cond = cond if cond else _empty
        self.step = step if step else _empty
        self.body = body if body else _empty

    @property
    def children(self) -> Tuple[AstNode, ...]:
        return self.init, self.cond, self.step, self.body

    def __str__(self) -> str:
        return 'for'


class StmtListNode(StmtNode):
    def __init__(self, *exprs: StmtNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.exprs = exprs

    @property
    def children(self) -> Tuple[StmtNode, ...]:
        return self.exprs

    def __str__(self) -> str:
        return '...'


_empty = StmtListNode()


class WhileNode(StmtNode):
    def __init__(self, cond: ExprNode, stmt_list: StmtNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.cond = cond
        self.stmt_list = stmt_list if stmt_list else _empty

    @property
    def children(self) -> Tuple['AstNode', ...]:
        return self.cond, self.stmt_list

    def __str__(self) -> str:
        return 'while'


class ArrayDeclarationNode(StmtNode):
    def __init__(self, vars_type: IdentNode, vars: IdentNode, value: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        checkNameAndException(str(vars), "array")
        self.vars_type = vars_type
        self.vars = vars
        self.value = value

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.vars_type, self.vars, self.value)

    def __str__(self) -> str:
        return 'array_declaration'

class ArrayNode(ExprNode):
    def __init__(self, name: IdentNode, value: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        checkNameAndException(str(name), "array")
        self.name = name
        self.value = value

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.name, self.value)

    def __str__(self) -> str:
        return 'array_index'

class ArgumentNode(StmtNode):
    def __init__(self, type_var: IdentNode, name: IdentNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        checkNameAndException(str(name), "argument in function declaration")
        self.type_var = type_var
        self.name = name


    @property
    def children(self) -> Tuple[IdentNode, ExprNode]:
        return self.type_var, self.name

    def __str__(self) -> str:
        return 'argument'



class FunctionDefinictionNode(StmtNode):
    def __init__(self, vars_type: IdentNode, name: IdentNode, *value: Tuple[ArgumentNode],
             row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.vars_type = vars_type
        self.name = name
        self.value = value

    @property
    def children(self) -> Tuple[ExprNode, ...]:
            # return self.vars_type, (*self.vars_list)
        return (self.vars_type, self.name) + self.value

    def __str__(self) -> str:
        return 'function_declaration'

class FunctionNode(StmtNode):
    def __init__(self, func: FunctionDefinictionNode, stmt_list: StmtListNode ,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.func = func
        self.list = stmt_list

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.func, self.list)

    def __str__(self) -> str:
        return 'function'

class ReturnNode(StmtNode):
    def __init__(self, expr : ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        #checkNameAndException(str(func), "function")
        self.expr = expr

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        # return self.func, (*self.params)
        return (self.expr,)

    def __str__(self) -> str:
        return 'return'