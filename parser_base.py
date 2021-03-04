from lark import Lark


'''
type_ident = (("int" | "float" ))    TO-DO   |  "bool" | "char"))
float_num -> <Дробное число>
int_num -> <Целое число>
num -> (("float_num" | "int_num"))
ident -> <Идентификатор>
group -> num | ident | '(' add ')'
mult -> group (('*' | '/' ) group)*
add -> mult (('+' | '-') mult)*
compare -> add (('<' | "<=" | '>' | ">=" | "==" | "!=") add)*
expr -> compare
init -> type_ident ident | type_ident ident = expr
assign -> ident "=" expr

if -> 'if' '(' compare ')' block ('else' block )?
while -> 'while' '(' compare ')' block

stmt -> assign | if | while  
stmts -> stmt*

block -> '{' stmts '}'

'''


def create_parser():
   parser = Lark.open("./syntax.lark", start='start')
   return parser