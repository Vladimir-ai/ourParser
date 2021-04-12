import parser_base
import os

from tests import working_test

if __name__ == '__main__':
    prog = open('tests/aaaaa.C', 'r').read()

    # prog = parser_base.parse("void d(int a[1]){}", True)
    # print(*parser_base.parse(prog).tree, sep=os.linesep)
    # parser_base.parse(prog)

    if working_test(True):
        print("It's ok")
    else:
        print("It isn't ok")