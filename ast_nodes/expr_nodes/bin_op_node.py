from typing import Tuple

from ast_nodes.expr_nodes.expr_node import ExprNode
from bin_op import BinOp


class BinOpNode(ExprNode):
    def __init__(self, operation: BinOp, arg1: ExprNode, arg2: ExprNode):
        super().__init__()
        self.operation = operation
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def children(self) -> Tuple[ExprNode, ExprNode]:
        return self.arg1, self.arg2

    def __str__(self):
        return self.operation.value
