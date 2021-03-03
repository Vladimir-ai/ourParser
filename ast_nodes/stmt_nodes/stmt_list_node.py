from typing import Tuple

from ast_nodes.ast_node import AstNode


class StmtList(AstNode):
    def __init__(self, *stmts: AstNode):
        super().__init__()
        self.stmts = stmts

    @property
    def children(self) -> Tuple[AstNode]:
        return self.stmts

    def __str__(self) -> str:
        return '...'
