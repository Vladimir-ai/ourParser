from lark import Lark, Transformer, InlineTransformer
from ast_node import *

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


class ASTBuilder(InlineTransformer):
   def __getattr__(self, item):
      def get_node(*args):
         return eval(''.join(x.capitalize() or '_' for x in item.split('_')) + 'Node')(*args)
      return get_node


def parse(prog: str, Debug=False) -> StmtListNode:
   parser = Lark.open("./syntax.lark", start='start') #, lexer='dynamic_complete'
   prog = parser.parse(prog)
   if Debug: print(prog)
   prog = ASTBuilder().transform(prog)
   return prog