from num_node import NumNode


class IntNumNode(NumNode):
    def __init__(self, num: int):
        super().__init__()
        self.num = int(num)

    def __str__(self) -> str:
        return str(self.num)