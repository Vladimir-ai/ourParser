from typing import Tuple

from ast_nodes.expr_nodes.expr_node import ExprNode
from ast_nodes.stmt_nodes.block_node import BlockNode
from stmt_node import StmtNode


class WhileNode(StmtNode):
    def __init__(self, condition: ExprNode, stmt: StmtNode):
        self.condition = condition
        self.stmt = stmt

    @property
    def children(self) -> Tuple[ExprNode, BlockNode]:
        return self.condition, self.then_stmt

    def __str__(self) -> str:
        return 'while'
