from num_node import NumNode


class DoubleNumNode(NumNode):
    def __init__(self, num: float):
        super().__init__()
        self.num = num

    def __str__(self) -> str:
        return str(self.num)