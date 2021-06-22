from typing import List, Union


class CodeLabel:
    def __init__(self):
        self.index = None

    def __str__(self):
        return 'IL_' + str(self.index)


class CodeLine:
    def __init__(self, code: str, *params: Union[str, CodeLabel], label: CodeLabel = None):
        self.code = code
        self.label = label
        self.params = params

    def __str__(self):
        line = ''
        if self.label:
            line += str(self.label) + ': '
        line += self.code
        for p in self.params:
            line += ' ' + str(p)
        return line


class CodeGenerator:
    def __init__(self):
        self.code_lines: List[CodeLine] = []

    def start(self) -> None:
        self.add('.assembly extern mscorlib {')
        self.add('.publickeytoken = (B0 3F 5F 7F 11 D5 0A 3A )                         // .?_....:')
        self.add('.ver 5:0:7:0')
        self.add('}')
        self.add('.assembly program')
        self.add('{')
        self.add('}')
        self.add('.class private auto ansi beforefieldinit Program extends [mscorlib]System.Object')
        self.add('{')

    def end(self) -> None:
        self.add('}')

    def add(self, code: str, label: str = None):
        if label:
            l = CodeLabel()
            l.index = label
            self.code_lines.append(CodeLine(code, label=l))
        else:
            self.code_lines.append(CodeLine(code))

    def __str__(self):
        return '\n'.join([str(line) for line in self.code_lines])
