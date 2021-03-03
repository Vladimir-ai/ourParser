from typing import Tuple

from ast_nodes.stmt_nodes.stmt_node import StmtNode
from ast_nodes.expr_nodes.ident_node import IdentNode
from ast_nodes.expr_nodes.expr_node import ExprNode


class AssignNode(StmtNode):
    def __init__(self, var: IdentNode, val: ExprNode):
        super(AssignNode, self).__init__()
        self.var = var
        self.val = val

    @property
    def children(self) -> Tuple[IdentNode, ExprNode]:
        return self.var, self.val

    def __str__(self) -> str:
        return "="