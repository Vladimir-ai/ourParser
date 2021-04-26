from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum
from utils import BinOp, BaseType
from semantic import IdentScope, TypeDesc, SemanticException, IdentDesc, BIN_OP_TYPE_COMPATIBILITY, TYPE_CONVERTIBILITY, \
    ArrayDesc


class KeyWords(Enum):
    RETURN = 'return'
    FOR = 'for'
    INT = 'int'
    CHAR = 'char'
    VOID = 'void'
    DOUBLE = 'double'
    FLOAT = 'float'


def checkNameIsKeywordAndRaiseException(name: str, text: str):
    if name.upper() in KeyWords.__dict__:
        raise Exception("Using keyword in name of " + text)


class AstNode(ABC):

    init_action: Callable[['AstNode'], None] = None

    def __init__(self, row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__()
        self.row = row
        self.line = line
        for k, v in props.items():
            setattr(self, k, v)
        self.node_type: Optional[TypeDesc] = None
        self.node_ident: Optional[IdentDesc] = None

    @property
    def children(self) -> Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self) -> str:
        pass

    def to_str_full(self):
        r = ''
        if self.node_ident:
            r = str(self.node_ident)
        elif self.node_type:
            r = str(self.node_type)
        return str(self) + (' : ' + r if r else '')

    def semantic_error(self, message: str):
        raise SemanticException(message, self.row, self.line)

    def semantic_check(self, scope: IdentScope) -> None:
        pass

    @property
    def tree(self) -> [str, ...]:
        res = [self.to_str_full()]
        children_temp = self.children
        for i, child in enumerate(children_temp):
            ch0, ch = '├', '│'
            if i == len(children_temp) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return tuple(res)

    def visit(self, func: Callable[['AstNode'], None]) -> None:
        func(self)
        map(func, self.children)

    def __getitem__(self, index):
        return self.children[index] if index < len(self.children) else None


class ExprNode(AstNode):
    pass

EMPTY_IDENT = IdentDesc('', TypeDesc.VOID)


class LiteralNode(ExprNode):
    def __init__(self, literal: str,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.literal = literal
        self.value = eval(literal)

    def semantic_check(self, scope: IdentScope) -> None:
        if isinstance(self.value, bool):
            self.node_type = TypeDesc.BOOL
        # проверка должна быть позже bool, т.к. bool наследник от int
        elif isinstance(self.value, str) and len(self.value) == 1:
            self.node_type = TypeDesc.CHAR
        elif isinstance(self.value, int):
            self.node_type = TypeDesc.INT
        elif isinstance(self.value, float):
            self.node_type = TypeDesc.FLOAT
        else:
            self.semantic_error('Неизвестный тип {} для {}'.format(type(self.value), self.value))

    def __str__(self) -> str:
        return '{0} ({1})'.format(self.literal, type(self.value).__name__)


class FactorNode(ExprNode):
    def __init__(self, operation: str, literal: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.literal = literal
        self.operation = operation

    @property
    def children(self) -> Tuple[ExprNode]:
        return [self.literal]

    def semantic_check(self, scope: IdentScope) -> None:
        self.literal.semantic_check(scope)

    def __str__(self) -> str:
        return f'uno {self.operation}'


class IdentNode(ExprNode):
    def __init__(self, name: str,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.name = str(name)

    def semantic_check(self, scope: IdentScope) -> None:
        ident = scope.get_ident(self.name)
        if ident is None:
            self.semantic_error('Идентификатор {} не найден'.format(self.name))
        self.node_type = ident.type
        self.node_ident = ident

    def __str__(self) -> str:
        return str(self.name)


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

    def semantic_check(self, scope: IdentScope) -> None:
        self.arg1.semantic_check(scope)
        self.arg2.semantic_check(scope)

        if self.arg1.node_ident is not None and self.arg2.node_ident is not None \
            and type(self.arg1.node_ident) != type(self.arg1.node_ident):
            self.semantic_error("BBBBBBBBBBBBBB")

        if self.arg1.node_type.is_simple or self.arg2.node_type.is_simple:
            compatibility = BIN_OP_TYPE_COMPATIBILITY[self.op]
            args_types = (self.arg1.node_type.base_type, self.arg2.node_type.base_type)
            if args_types in compatibility:
                self.node_type = TypeDesc.from_base_type(compatibility[args_types])
                return

            if self.arg2.node_type.base_type in TYPE_CONVERTIBILITY:
                for arg2_type in TYPE_CONVERTIBILITY[self.arg2.node_type.base_type]:
                    args_types = (self.arg1.node_type.base_type, arg2_type)
                    if args_types in compatibility:
                        self.arg2 = type_convert(self.arg2, TypeDesc.from_base_type(arg2_type))
                        self.node_type = TypeDesc.from_base_type(compatibility[args_types])
                        return
            if self.arg1.node_type.base_type in TYPE_CONVERTIBILITY:
                for arg1_type in TYPE_CONVERTIBILITY[self.arg1.node_type.base_type]:
                    args_types = (arg1_type, self.arg2.node_type.base_type)
                    if args_types in compatibility:
                        self.arg1 = type_convert(self.arg1, TypeDesc.from_base_type(arg1_type))
                        self.node_type = TypeDesc.from_base_type(compatibility[args_types])
                        return

        if not self.arg1.node_type.is_simple and not self.arg2.node_type.is_simple:
            if self.arg1.node_type.base_type == self.arg2.node_type.base_type:
                return

        self.semantic_error("Оператор {} не применим к типам ({}, {})".format(
            self.op, self.arg1.node_type, self.arg2.node_type
        ))

    def __str__(self) -> str:
        return str(self.op.value)


class StmtNode(ExprNode):
    def to_str_full(self):
        return str(self)


class VarsDeclNode(StmtNode):
    def __init__(self, vars_type: IdentNode, *vars_list: Tuple[AstNode, ...],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.vars_type = vars_type
        self.vars_list = vars_list

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.vars_type,) + self.vars_list

    def semantic_check(self, scope: IdentScope) -> None:
        if str(self.vars_type).upper() not in BaseType.__dict__:
            self.semantic_error(f"Unknown type {self.vars_type}")
        for var in self.vars_list:
            var_node: IdentNode = var.var if isinstance(var, AssignNode) else var
            try:
                scope.add_ident(IdentDesc(var_node.name, TypeDesc.from_str(str(self.vars_type))))
            except SemanticException as e:
                var_node.semantic_error(e.message)
            var.semantic_check(scope)
        self.node_type = TypeDesc.VOID

    def __str__(self) -> str:
        return 'var'


class CallNode(StmtNode):
    def __init__(self, func: IdentNode, *params: Tuple[ExprNode],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        checkNameIsKeywordAndRaiseException(str(func), "function")
        self.func = func
        self.params = params

    @property
    def children(self) -> Tuple[IdentNode, ...]:
        # return self.func, (*self.params)
        return (self.func,) + self.params

    def semantic_check(self, scope: IdentScope) -> None:
        func = scope.get_ident(self.func.name)
        if func is None:
            self.semantic_error('Функция {} не найдена'.format(self.func.name))
        if not func.type.func:
            self.semantic_error('Идентификатор {} не является функцией'.format(func.name))
        if len(func.type.params) != len(self.params):
            self.semantic_error('Кол-во аргументов {} не совпадает (ожидалось {}, передано {})'.format(
                func.name, len(func.type.params), len(self.params)
            ))
        params = []
        error = False
        decl_params_str = fact_params_str = ''
        for i in range(len(self.params)):
            param: ExprNode = self.params[i]
            param.semantic_check(scope)
            if (len(decl_params_str) > 0):
                decl_params_str += ', '
            decl_params_str += str(func.type.params[i])
            if (len(fact_params_str) > 0):
                fact_params_str += ', '
            fact_params_str += str(param.node_type)
            try:
                params.append(type_convert(param, func.type.params[i]))
            except:
                error = True
        if error:
            self.semantic_error('Фактические типы ({1}) аргументов функции {0} не совпадают с формальными ({2})\
                                    и не приводимы'.format(
                func.name, fact_params_str, decl_params_str
            ))
        else:
            self.params = tuple(params)
            self.func.node_type = func.type
            self.func.node_ident = func
            self.node_type = func.type.return_type


    def __str__(self) -> str:
        return 'call'


class AssignNode(StmtNode):
    def __init__(self, var: IdentNode, val: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.var = var
        self.val = val

    @property
    def children(self) -> Tuple[IdentNode, ExprNode]:
        return self.var, self.val

    def semantic_check(self, scope: IdentScope) -> None:
        self.var.semantic_check(scope)
        self.val.semantic_check(scope)

        if self.var.node_ident is not None and self.val.node_ident is not None \
                and type(self.var.node_ident) != type(self.val.node_ident):
            self.semantic_error("AAAAAAAA")

        self.val = type_convert(self.val, self.var.node_type, self, 'присваиваемое значение')
        self.node_type = self.var.node_type

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

    def semantic_check(self, scope: IdentScope) -> None:
        self.cond.semantic_check(scope)
        self.cond = type_convert(self.cond, TypeDesc.BOOL, None, 'условие')
        self.then_stmt.semantic_check(IdentScope(scope))
        if self.else_stmt:
            self.else_stmt.semantic_check(IdentScope(scope))
        self.node_type = TypeDesc.VOID

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

    def semantic_check(self, scope: IdentScope) -> None:
        scope = IdentScope(scope)
        self.init.semantic_check(scope)
        if self.cond == _empty:
            self.cond = LiteralNode('true')
        self.cond.semantic_check(scope)
        self.cond = type_convert(self.cond, TypeDesc.BOOL, None, 'условие')
        self.step.semantic_check(scope)
        self.body.semantic_check(IdentScope(scope))
        self.node_type = TypeDesc.VOID

    def __str__(self) -> str:
        return 'for'


class StmtListNode(StmtNode):
    def __init__(self, *exprs: StmtNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.exprs = exprs
        self.program = False

    @property
    def children(self) -> Tuple[StmtNode, ...]:
        return self.exprs

    def semantic_check(self, scope: IdentScope) -> None:
        if not self.program:
            scope = IdentScope(scope)
        for expr in self.exprs:
            expr.semantic_check(scope)
        self.node_type = TypeDesc.VOID

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

    def semantic_check(self, scope: IdentScope) -> None:
        scope = IdentScope(scope)
        if self.cond == _empty:
            self.cond = LiteralNode('true')
        self.cond.semantic_check(scope)
        self.cond = type_convert(self.cond, TypeDesc.BOOL, None, 'условие')
        self.stmt_list.semantic_check(IdentScope(scope))
        self.node_type = TypeDesc.VOID

    def __str__(self) -> str:
        return 'while'


class ArrayDeclarationNode(StmtNode):
    def __init__(self, type_var: IdentNode, name: IdentNode, value: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.type_var = type_var
        self.name = name
        self.value = value

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.type_var, self.name, self.value)

    def semantic_check(self, scope: IdentScope) -> None:
        if str(self.name).upper() in BaseType.__dict__:
            self.semantic_error("Using keyword in name of array")

        if str(self.type_var).upper() not in BaseType.__dict__:
            self.semantic_error(f"Unknown type {self.type_var}")

        try:
            self.value.semantic_check(scope)
            scope.add_ident(ArrayDesc(str(self.name), TypeDesc.arr_from_str(str(self.type_var)), type_convert(self.value, TypeDesc.INT, self)))
        except SemanticException as e:
            self.semantic_error(e.message)
        self.node_type = TypeDesc.arr_from_str(str(self.type_var))

    def __str__(self) -> str:
        return 'array_declaration'


class ArrayIndexingNode(ExprNode):
    def __init__(self, name: IdentNode, value: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.name = name
        self.value = value

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.name, self.value)

    def semantic_check(self, scope: IdentScope) -> None:
        if str(self.name).upper() in BaseType.__dict__:
            self.semantic_error("Using keyword in name of array")
        self.name.semantic_check(scope)
        self.value.semantic_check(scope) #check return type
        curr_ident = scope.get_ident(str(self.name))
        if not isinstance(curr_ident, ArrayDesc):
            self.semantic_error(f"{self.name} is not an array")

        self.node_type = scope.get_ident(str(self.name)).toIdentDesc().type

    def __str__(self) -> str:
        return 'array_index'


class ArgumentNode(StmtNode):
    def __init__(self, type_var: IdentNode, name: IdentNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.type_var = type_var
        self.name = name

    @property
    def children(self) -> Tuple[IdentNode, ExprNode]:
        return self.type_var, self.name

    def semantic_check(self, scope: IdentScope) -> None:
        if str(self.name).upper() in KeyWords.__dict__:
            self.semantic_error("Using keyword in the name of argument in function declaration")
        try:
            self.name.node_ident = scope.add_ident(IdentDesc(self.name.name, TypeDesc.from_str(str(self.type_var))));
        except:
            raise self.name.semantic_error(f'Параметр {self.name.name} уже объявлен')
        self.node_type = TypeDesc.VOID

    def __str__(self) -> str:
        return 'argument'


class ArgumentListNode(StmtNode):
    def __init__(self, *arguments: Tuple[ArgumentNode],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.arguments = arguments

    @property
    def children(self) -> Tuple[ArgumentNode]:
        return self.arguments

    def __str__(self) -> str:
        return 'argument_list'


class ReturnTypeNode(AstNode):
    def __init__(self, type: IdentNode, isArr: Optional[str] = None,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.type = type
        self.isArr = isArr

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        return [self.type]

    def semantic_check(self, scope: IdentScope) -> None:
        if self.type is None:
            self.semantic_error(f"Неизвестный тип: {type}")

    def __str__(self) -> str:
        return f'return type {"array" if self.isArr is not None else ""}'


class FunctionNode(StmtNode):
    def __init__(self, type: ReturnTypeNode, name: IdentNode, argument_list: ArgumentListNode, stmt_list: StmtListNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.type = type
        self.name = name
        self.argument_list = argument_list
        self.list = stmt_list

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        return self.type, self.name, self.argument_list, self.list

    def semantic_check(self, scope: IdentScope) -> None:
        if scope.curr_func:
            self.semantic_error("Объявление функции ({}) внутри другой функции не поддерживается".format(self.name.name))
        parent_scope = scope
        self.type.semantic_check(scope)
        scope = IdentScope(scope)

        # временно хоть какое-то значение, чтобы при добавлении параметров находить scope функции
        scope.func = EMPTY_IDENT
        params = []
        for param in self.argument_list.children:
            # при проверке параметров происходит их добавление в scope
            param.semantic_check(scope)
            if isinstance(param, ArrayDeclarationNode):
                params.append(TypeDesc.arr_from_str(str(param.type_var)))
            else:
                params.append(TypeDesc.from_str(str(param.type_var)))

        if self.type.isArr:
            type_ = TypeDesc(None, TypeDesc.arr_from_str(str(self.type.type)), tuple(params))
            func_ident = ArrayDesc(self.name.name, type_, 1)
        else:
            type_ = TypeDesc(None, TypeDesc.from_str(str(self.type.type)), tuple(params))
            func_ident = IdentDesc(self.name.name, type_)
        scope.func = func_ident
        self.name.node_type = type_
        try:
            self.name.node_ident = parent_scope.curr_global.add_ident(func_ident)
        except SemanticException as e:
            self.name.semantic_error("Повторное объявление функции {}".format(self.name.name))
        self.list.semantic_check(scope)
        self.node_type = TypeDesc.VOID

    def __str__(self) -> str:
        return 'function'


class ReturnNode(StmtNode):
    def __init__(self, expr: Optional[ExprNode] = None,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        # checkNameAndException(str(func), "function")
        self.expr = expr

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        return [self.expr] if self.expr else list()

    def semantic_check(self, scope: IdentScope) -> None:
        self.expr.semantic_check(IdentScope(scope))
        func = scope.curr_func
        if func is None:
            self.semantic_error('Оператор return применим только к функции')
        self.expr = type_convert(self.expr, func.func.type.return_type, self, 'возвращаемое значение')
        self.node_type = TypeDesc.VOID

    def __str__(self) -> str:
        return 'return'


class _GroupNode(AstNode):
    """Класс для группировки других узлов (вспомогательный, в синтаксисе нет соотвествия)
    """

    def __init__(self, name: str, *childs: AstNode,
                 row: Optional[int] = None, col: Optional[int] = None, **props) -> None:
        super().__init__(row=row, col=col, **props)
        self.name = name
        self._childs = childs

    def __str__(self) -> str:
        return self.name

    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return self._childs


class TypeConvertNode(ExprNode):
    """Класс для представления в AST-дереве операций конвертации типов данных
       (в языке программирования может быть как expression, так и statement)
    """
    def __init__(self, expr: ExprNode, type_: TypeDesc,
                 row: Optional[int] = None, col: Optional[int] = None, **props) -> None:
        super().__init__(row=row, col=col, **props)
        self.expr = expr
        self.type = type_
        self.node_type = type_

    def __str__(self) -> str:
        return 'convert'

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return _GroupNode(str(self.type), self.expr),


def type_convert(expr: ExprNode, type_: TypeDesc, except_node: Optional[AstNode] = None,
                 comment: Optional[str] = None) -> ExprNode:
    """Метод преобразования ExprNode узла AST-дерева к другому типу
    :param expr: узел AST-дерева
    :param type_: требуемый тип
    :param except_node: узел, у которого будет исключение
    :param comment: комментарий
    :return: узел AST-дерева c операцией преобразования
    """

    if expr.node_type is None:
        except_node.semantic_error('Тип выражения не определен')
    if expr.node_type == type_:
        return expr
    if expr.node_type.is_simple and type_.is_simple and \
            expr.node_type.base_type in TYPE_CONVERTIBILITY and type_.base_type in TYPE_CONVERTIBILITY[
        expr.node_type.base_type]:
        return TypeConvertNode(expr, type_)
    else:
        (except_node if except_node else expr).semantic_error('Тип {0}{2} не конвертируется в {1}'.format(
            expr.node_type, type_, ' ({})'.format(comment) if comment else ''
        ))


