from ast_nodes.ast_node import AstNode


class IntNum(AstNode):
    def __init__(self, num: int):
        super().__init__()
        self.num = int(num)

    def __str__(self) -> str:
        return str(self.num)