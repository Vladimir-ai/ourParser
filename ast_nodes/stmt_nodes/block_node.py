from typing import Tuple

from stmt_node import StmtNode


class BlockNode(StmtNode):
    def __init__(self, *stmts: StmtNode):
        super().__init__()
        self.stmts = stmts

    @property
    def children(self) -> Tuple[StmtNode]:
        return self.stmts

    def __str__(self) -> str:
        return '{...}'

