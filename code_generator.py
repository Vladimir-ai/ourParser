from typing import List, Dict


INT_POINTER_CONST = "@int.0.0"
CHAR_POINTER_CONST = "@char.0.0"
FLOAT_POINTER_CONST = "@float.0.0"


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
        self.code_lines.append(CodeLine("declare i32 @scanf(i8*, ...) nounwind\n"))

        self.code_lines.append(CodeLine("declare void @llvm.memcpy.p0i32.p0i32.i32(i32*, i32*, i32, i1)"))
        self.code_lines.append(CodeLine("declare void @llvm.memcpy.p0i1.p0i1.i32(i1*, i1*, i32, i1)"))
        self.code_lines.append(CodeLine("declare void @llvm.memcpy.p0i8.p0i8.i32(i8*, i8*, i32, i1)"))
        self.code_lines.append(CodeLine("declare void @llvm.memcpy.p0double.p0double.i32(double*, double*, i32, i1)\n"))

        self.code_lines.append(CodeLine(f"{INT_POINTER_CONST} = global i32 0"))
        self.code_lines.append(CodeLine(f"{CHAR_POINTER_CONST} = global i8 0"))
        self.code_lines.append(CodeLine(f"{FLOAT_POINTER_CONST} = global double 0.0\n"))

        self.code_lines.append(CodeLine("@formatInt = private constant [4 x i8] c\"%d\\0A\\00\""))
        self.code_lines.append(CodeLine("@formatFloat = private constant [4 x i8] c\"%f\\0A\\00\""))
        self.code_lines.append(CodeLine("@formatChar = private constant [4 x i8] c\"%c\\0A\\00\"\n"))

        self.code_lines.append(CodeLine("@inputFloat = private constant [4 x i8] c\"%lf\\00\""))
        self.code_lines.append(CodeLine("@inputChar = private constant [3 x i8] c\"%c\\00\""))
        self.code_lines.append(CodeLine("@inputInt = private constant [3 x i8] c\"%d\\00\"\n"))

    def add(self, code: str):
        self.code_lines.append(CodeLine(code))

    def addVarIndex(self, var_name: str):
        if str(var_name) in self.var_counter:
            self.var_counter[str(var_name)] += 1
        else:
            self.var_counter[str(var_name)] = 1

    def getVarIndex(self, var_name:str)->int:
        if var_name not in self.var_counter:
            return 0
        return self.var_counter[str(var_name)]

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
