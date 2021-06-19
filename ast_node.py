from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum
from utils import BinOp, BaseType, getLLVMtype, getBinOp, getConvOp, isBuiltinFunc
from semantic import IdentScope, TypeDesc, SemanticException, IdentDesc, BIN_OP_TYPE_COMPATIBILITY, TYPE_CONVERTIBILITY, \
    ArrayDesc

from code_generator import CodeGenerator


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

    def __init__(self, line: Optional[int] = None, column: Optional[int] = None, **props):
        super().__init__()
        self.line = line
        self.column = column
        for k, v in props.items():
            setattr(self, k, v)
        self.node_type: Optional[TypeDesc] = None
        self.node_ident: Optional[IdentDesc] = None

    @property
    def children(self) -> Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self) -> (str, int):
        pass

    def to_str_full(self):
        r = ''
        if self.node_ident:
            r = str(self.node_ident)
        elif self.node_type:
            r = str(self.node_type)
        return str(self) + (' : ' + r if r else '')

    def semantic_error(self, message: str):
        raise SemanticException(message, self.line, self.column)

    def semantic_check(self, scope: IdentScope) -> None:
        pass

    def to_llvm(self, gen: CodeGenerator):
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

class StmtListNode:
    pass

class ExprNode(AstNode):
    def load(self, gen: CodeGenerator) -> str:
        pass

EMPTY_IDENT = IdentDesc('', TypeDesc.VOID)


class LiteralNode(ExprNode):
    def __init__(self, literal: str,
                 line: Optional[int] = None, column: Optional[int] = None, **props):
        super().__init__(line=line, column=column, **props)
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

    def load(self, gen: CodeGenerator) -> str:
        if self.node_type.base_type == BaseType.CHAR:
            return ord(self.value)

        return self.value

    def __str__(self) -> str:
        return '{0} ({1})'.format(self.literal, type(self.value).__name__)


class FactorNode(ExprNode):
    def __init__(self, operation: str, literal: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.literal = literal
        self.operation = operation

    @property
    def children(self) -> list[ExprNode]:
        return [self.literal]

    def semantic_check(self, scope: IdentScope) -> None:
        self.literal.semantic_check(scope)
        self.node_type = self.literal.node_type

    def load(self, gen: CodeGenerator) -> str:
        return f"{self.operation}{self.literal.load(gen)}"

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

    def load(self, gen:CodeGenerator) -> str:
        gen.add(f"%{self.name}.{gen.getVarIndex(self.name)} = load {getLLVMtype(self.node_type.base_type)}, {getLLVMtype(self.node_type.base_type)}* %{self.name}")
        gen.addVarIndex(self.name)
        return f"%{self.name}.{gen.getVarIndex(self.name) - 1}"

    def __str__(self) -> str:
        return str(self.name)


class BinOpNode(ExprNode):
    def __init__(self, op: BinOp, arg1: ExprNode, arg2: ExprNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.is_simple = (isinstance(arg1, LiteralNode) or (isinstance(arg1, BinOpNode) and arg1.is_simple)) \
                            and (isinstance(arg2, LiteralNode) or (isinstance(arg2, BinOpNode) and arg2.is_simple))

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
                for arg2_type in TYPE_CONVERTIBILITY:
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

    def load(self, gen: CodeGenerator) -> str:

        if self.is_simple:
            return eval(f"{self.arg1.load(gen)}{self.op.value}{self.arg2.load(gen)}")

        arg1 = self.arg1.load(gen)
        arg2 = self.arg2.load(gen)

        ret = f"%{gen.getTempVar()}"
        gen.add(f"{ret} = {getBinOp(self.op, self.arg1.node_type.base_type)} {getLLVMtype(self.arg1.node_type.base_type)} "
                f"{arg1}, {arg2}")
        gen.addTempVarIndex()
        return ret

    def to_llvm(self, gen: CodeGenerator):
        pass

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

    def to_llvm(self, gen: CodeGenerator):
        val = "0" if BaseType(self.vars_type.name) != BaseType.FLOAT else "0.0"
        for node in self.vars_list:
            if isinstance(node, AssignNode):
                gen.add(f"%{node.var.name} = alloca {getLLVMtype(self.vars_type.name)}")
                gen.add(f"store {getLLVMtype(self.vars_type.name)} {val}, {getLLVMtype(self.vars_type.name)}* %{node.var.name}")
                node.to_llvm(gen)
            if isinstance(node, IdentNode):
                gen.add(f"%{node.name} = alloca {getLLVMtype(self.vars_type.name)}")
                gen.add(f"store {getLLVMtype(self.vars_type.name)} {val}, {getLLVMtype(self.vars_type.name)}* %{node.name}")

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

    def to_llvm(self, gen: CodeGenerator):
        self.load(gen)

    def load(self, gen: CodeGenerator) -> str:
        result = f"%call.{self.func.name}.{gen.getVarIndex(f'call.{self.func.name}')}"
        gen.addVarIndex(f'call.{self.func.name}')

        if len(self.params) == 0:
            gen.add(f"{result} = call {getLLVMtype(self.node_type.base_type)} @{self.func.name}()")
            return result

        if len(self.params) == 1 and isBuiltinFunc(self.func.name):
            var0 = self.params[0].load(gen)

            if self.func.name == "print_float" and self.params[0].node_type.base_type == BaseType.FLOAT:
                gen.add(f"{result} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds "
                        f"([4 x i8], [4 x i8]* @formatFloat, i32 0, i32 0), double {var0})")

            elif self.func.name == "print_int" and self.params[0].node_type.base_type == BaseType.INT:
                gen.add(f"{result} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds "
                        f"([4 x i8], [4 x i8]* @formatInt, i32 0, i32 0), i32 {var0})")

            elif self.func.name == "print_char" and self.params[0].node_type.base_type == BaseType.CHAR:
                gen.add(f"{result} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds "
                        f"([4 x i8], [4 x i8]* @formatChar, i32 0, i32 0), i8 {var0})")
                gen.addTempVarIndex()

            return result

        gen.add(f"{result} = call {getLLVMtype(self.node_type.base_type)} @{self.func.name}"
                f"({', '.join(f'{getLLVMtype(param.node_type)} {param.load(gen)}' for param in self.params)})")

        return result

        #TODO for multiple vars

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
            self.semantic_error("incompatible types")

        self.val = type_convert(self.val, self.var.node_type, self, 'присваиваемое значение')
        self.node_type = self.var.node_type

    def to_llvm(self, gen: CodeGenerator) -> None:
        add = "fadd" if self.node_type.base_type == BaseType.FLOAT else "add"
        if isinstance(self.val, LiteralNode):
            gen.add(f"%{self.var.name}.{gen.getVarIndex(self.var.name)} = {add} {getLLVMtype(self.node_type.base_type)} "
                    f"{0.0 if self.node_type.base_type == BaseType.FLOAT else 0}, "
                    f"{self.val.value if self.node_type.base_type != BaseType.CHAR else ord(self.val.value)}")

            gen.addVarIndex(self.var.name)
            gen.add(f"store {getLLVMtype(self.node_type.base_type)} %{self.var.name}.{gen.getVarIndex(self.var.name) - 1}, "
                    f"{getLLVMtype(self.node_type.base_type)}* %{self.var.name}")

        elif isinstance(self.val, ExprNode):
            res = self.val.load(gen)
            gen.add(f"store {getLLVMtype(self.val.node_type.base_type)} {res}, "
                f"{getLLVMtype(self.var.node_type.base_type)}* %{self.var.name}")

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

    def to_llvm(self, gen: CodeGenerator)->None:
        condRes = self.cond.load(gen)
        eqLabel = f"IfTrue.0.{gen.getVarIndex('if')}"
        neqLabel = f"IfFalse.0.{gen.getVarIndex('if')}"
        resLabel = f"IfEnd.0.{gen.getVarIndex('if')}"
        gen.addVarIndex('if')

        gen.add(f"br i1 {condRes}, label %{eqLabel}, label %{neqLabel if self.else_stmt is not None else resLabel}\n")
        gen.add(f"{eqLabel}:")

        self.then_stmt.to_llvm(gen)
        gen.add(f"br label %{resLabel}")

        if self.else_stmt is not None:
            gen.add(f"\n{neqLabel}:")
            self.else_stmt.to_llvm(gen)
            gen.add(f"br label %{resLabel}")

        gen.add(f"\n{resLabel}:")

    def __str__(self) -> str:
        return 'if'


class ForNode(AstNode):
    def __init__(self, init: StmtListNode, cond: ExprNode,
                 step: StmtListNode, body: Union[StmtNode, None] = None,
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

    def to_llvm(self, gen: CodeGenerator):
        varIndex = gen.getVarIndex('for')
        forHeader = f"for.head.{varIndex}"
        forCond = f"for.cond.{varIndex}"
        forBody = f"for.body.{varIndex}"
        forHatch = f"for.hatch.{varIndex}"
        forExit = f"for.exit.{varIndex}"

        gen.add(f"br label %{forHeader}\n")
        gen.add(f"{forHeader}:")
        self.init.to_llvm(gen)
        gen.add(f"br label %{forCond}")

        gen.add(f"{forCond}:") #for condition
        condRes = self.cond.load(gen)

        gen.add(f"br i1 {condRes}, label %{forBody}, label %{forExit}\n")

        gen.add(f"{forBody}:") #for body
        self.body.to_llvm(gen)
        gen.add(f"br label %{forHatch}\n")

        gen.add(f"{forHatch}:")
        self.step.to_llvm(gen)
        gen.add(f"br label %{forCond}\n")

        gen.add(f"{forExit}:")

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

    def to_llvm(self, gen: CodeGenerator):
        for child in self.children:
            child.to_llvm(gen)

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

    def to_llvm(self, gen: CodeGenerator):
        condLabel = f"whihe.cond.{gen.getVarIndex('while')}"
        bodyLabel = f"whihe.body.{gen.getVarIndex('while')}"
        exitLabel = f"while.exit.{gen.getVarIndex('while')}"

        gen.addVarIndex('while')
        gen.add(f"br label %{condLabel}\n")
        gen.add(f"{condLabel}:")

        condVar = self.cond.load(gen)
        gen.add(f"br i1 {condVar}, label %{bodyLabel}, label %{exitLabel}\n")

        gen.add(f"{bodyLabel}:")
        self.stmt_list.to_llvm(gen)
        gen.add(f"br label %{condLabel}\n")

        gen.add(f"{exitLabel}:")

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

    def load(self, gen: CodeGenerator) -> str:
        return f"{getLLVMtype(self.type_var.name)} %c{self.name.name}"

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

    def load(self, gen: CodeGenerator) -> str:
        return ", ".join(f"{arg.load(gen)}" for arg in self.arguments)

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

    #TODO return

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

    def to_llvm(self, gen: CodeGenerator) -> None:
        code = f"define {getLLVMtype(self.type.type.name)} @{self.name.name}" \
               f"({self.argument_list.load(gen)}) "'{'
        gen.add(code)

        if len(self.argument_list.children) > 0:
            gen.add("\n".join([f"%{arg.name} = alloca {getLLVMtype(arg.type_var.name)}" for arg in self.argument_list.children]))
            gen.add("\n".join([f"store {getLLVMtype(arg.type_var.name)} %c{arg.name}, {getLLVMtype(arg.type_var.name)}* %{arg.name}" for arg in self.argument_list.children]))
        self.list.to_llvm(gen)

        if next((x for x in self.list.children if isinstance(x, ReturnNode)), None) is None:
            gen.add("ret void")
        gen.add("}\n")

    def __str__(self) -> str:
        return 'function'


class ReturnNode(ExprNode):
    def __init__(self, expr: Optional[ExprNode] = None,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        # checkNameAndException(str(func), "function")
        self.expr = expr

    @property
    def children(self) -> Tuple[ExprNode, ...]:
        return [self.expr] if self.expr else list()

    def semantic_check(self, scope: IdentScope) -> None:
        func = scope.curr_func
        if func is None:
            self.semantic_error('Оператор return применим только к функции')

        if self.expr is not None:
            self.expr.semantic_check(IdentScope(scope))
            self.expr = type_convert(self.expr, func.func.type.return_type, self, 'возвращаемое значение')

        self.node_type = TypeDesc.VOID

    def to_llvm(self, gen: CodeGenerator):
        res = self.expr.load(gen) if self.expr is not None else "void"
        gen.add(f"ret {getLLVMtype(self.expr.node_type)} {res}")

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

    def load(self, gen: CodeGenerator) -> str:
        var = self.expr.load(gen)
        aa = getConvOp(self.expr.node_type.base_type, self.node_type.base_type)
        gen.add(f"%{gen.getTempVar()} = {aa} "
                f"{getLLVMtype(self.expr.node_type.base_type)} "
                f"{var} to {getLLVMtype(self.type)}")

        var = f"%{gen.getTempVar()}"
        gen.addTempVarIndex()
        return var

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
            expr.node_type.base_type in TYPE_CONVERTIBILITY and type_.base_type in TYPE_CONVERTIBILITY:
        return TypeConvertNode(expr, type_)
    else:
        (except_node if except_node else expr).semantic_error('Тип {0}{2} не конвертируется в {1}'.format(
            expr.node_type, type_, ' ({})'.format(comment) if comment else ''
        ))


