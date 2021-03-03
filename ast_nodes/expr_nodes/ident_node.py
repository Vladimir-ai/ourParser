from ast_nodes.expr_nodes.expr_node import ExprNode


class IdentNode(ExprNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return str(self.name)