from typing import Tuple

from ast_nodes.expr_nodes.expr_node import ExprNode
from ast_nodes.stmt_nodes.block_node import BlockNode
from stmt_node import StmtNode


class IfNode(StmtNode):
    def __init__(self, condition: ExprNode, then_stmt: BlockNode, else_stmt: BlockNode):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    @property
    def children(self) -> Tuple[ExprNode, BlockNode, BlockNode]:
        return (self.condition, self.then_stmt) + ((self.else_stmt) if self.else_stmt else tuple())

    def __str__(self) -> str:
        return 'if'
