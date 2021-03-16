from abc import ABC, abstractmethod
from typing import Tuple, Callable, List


class AstNode(ABC):
    @property
    def children(self) -> Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> [str, ...]:
        res = [str(self)]
        children = self.children
        for i, child in enumerate(children):
            ch0, ch = '├', '│'
            if i == len(children) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None]) -> None:
        func(self)
        map(func, self.children)

    def __getitem__(self, item):
        return self.children[item] if item < len(self.children) else None


class StmtNode(AstNode, ABC):
    pass


class StmtListNode(AstNode):
    def __init__(self, stmts: List[StmtNode]):
        super().__init__()
        self.stmts = tuple(stmts)

    @property
    def children(self) -> Tuple[StmtNode, ...]:
        return self.stmts

    def __str__(self) -> str:
        return '...'


class ExprNode(AstNode, ABC):
    pass


class NumNode(ExprNode, ABC):
    pass


class IntNumNode(NumNode):
    def __init__(self, num: int):
        super().__init__()
        self.num = int(num)

    def __str__(self) -> str:
        return str(self.num)


class FloatNumNode(NumNode):
    def __init(self, num: float):
        super().__init__()
        self.num = num

    def __str__(self) -> str:
        return str(self.num)


class TypeIdentNode(AstNode):
    def __init__(self, type: str):
        super().__init__()
        self.type = type

    def __str__(self) -> str:
        return str(self.type)


class IdentNode(AstNode):
    def __init__(self, name: List[ExprNode]):
        super().__init__()
        self.name = name[0]

    def __str__(self) -> str:
        return str(self.name)


class AssignNode(StmtNode):
    def __init__(self, args: list[AstNode]):
        super().__init__()
        self.ident = args[0]
        self.expr = args[1]

    @property
    def children(self) -> Tuple[IdentNode, ExprNode]:
        return self.ident, self.expr

    def __str__(self) -> str:
        return "="