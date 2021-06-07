from typing import List, Dict


class CodeLine:
    def __init__(self, code: str):
     self.code = code

    def __str__(self):
        return self.code + "\n"


class CodeGenerator:
    def __init__(self):
        self.code_lines: List[CodeLine] = []
        self.var_counter: Dict[str, int] = {}

    def start(self):
        self.code_lines.append(CodeLine("declare i32 @printf(i8*, ...) nounwind"))
        self.code_lines.append(CodeLine("@formatInt = private constant [4 x i8] c\"%d\\0A\\00\""))
        self.code_lines.append(CodeLine("@formatFloat = private constant [4 x i8] c\"%f\\0A\\00\""))
        self.code_lines.append(CodeLine("@formatChar = private constant [4 x i8] c\"%c\\0A\\00\""))

    def add(self, code: str):
        self.code_lines.append(CodeLine(code))

    def addVarIndex(self, var_name: str):
        if var_name in self.var_counter:
            self.var_counter[var_name] += 1
        else:
            self.var_counter[var_name] = 1

    def getVarIndex(self, var_name:str)->int:
        if var_name not in self.var_counter:
            return 0
        return self.var_counter[var_name]

    def getTempVar(self) -> str:
        temp = "temp"
        return f"temp.0.{self.getVarIndex(temp)}"

    def addTempVarIndex(self):
        self.addVarIndex("temp")

    def __str__(self):
        code = ""
        for line in self.code_lines:
            code += str(line)

        return code
