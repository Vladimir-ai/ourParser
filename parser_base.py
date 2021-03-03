import inspect
from contextlib import suppress

import pyparsing as pp
from pyparsing import pyparsing_common as ppc

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
    int_keyword = pp.Keyword("int")
    double_keyword = pp.Keyword("double")
    char_keyword = pp.Keyword("char")
    bool_keyword = pp.Keyword("bool")
    if_keyword = pp.Keyword("if")
    else_keyword = pp.Keyword("else")
    return_keyword = pp.Keyword("return")
    while_keyword = pp.Keyword("while")

    type_ident = int_keyword | double_keyword | char_keyword | bool_keyword

    int_num = ppc.integer
    double_num = ppc.real
    ident = ppc.identifier

    L_PAR, R_PAR = pp.Literal('('), pp.Literal(')')
    L_BRAC, R_BRAC = pp.Literal('{'), pp.Literal('}')
    ASSIGN = pp.Literal('=') #add *= and etc. later
    MULT, ADD = pp.oneOf('* /'), pp.oneOf('+ -')
    BOOL_OP = pp.oneOf('|| && !')
    COMPARE = pp.oneOf('> < <= >= == !=')

    bool_op = pp.Forward()
    stmts = pp.Forward()

    num = int_num | double_num
    block = L_BRAC + stmts + R_BRAC
    group = ident | num | L_PAR + bool_op + R_PAR
    mult = group + pp.ZeroOrMore(MULT + group)
    add = (mult + pp.ZeroOrMore(ADD + mult))
    compare = add + pp.ZeroOrMore(COMPARE + add)
    bool_op = compare + pp.ZeroOrMore(BOOL_OP + compare)
    expr = bool_op

    stmt = pp.Forward()
    if_stmt = if_keyword + L_PAR + expr + R_PAR +\
              block + pp.Optional(else_keyword + block)
    while_stmt = while_keyword + L_PAR + expr + R_PAR + block
    assign = ident + ASSIGN + expr
    init_stmt = type_ident + ident + ASSIGN + expr

    stmt << (if_stmt | while_stmt | assign | init_stmt)
    stmts << pp.ZeroOrMore(stmt)

    program = stmts.ignore(pp.cStyleComment).ignore(pp.cppStyleComment) + pp.StringEnd()
    start = program


    return start


parser = create_parser()


def parse(prog: str):
    return parser.parseString(str(prog))







