import parser_base
import semantic
import os
from code_generator import CodeGenerator

from tests import working_test

if __name__ == '__main__':
    prog = open('tests/bbbb.c', 'r').read()

    # prog = parser_base.parse("void d(int a[1]){}", True)
    # print(*parser_base.parse(prog).tree, sep=os.linesep)
    # parser_base.parse(prog)

    if working_test(False):
        print("All tests have been passed")
    else:
        print("It isn't ok")

    tree = parser_base.parse(prog)
    print('ast_tree:')
    print(*tree.tree, sep=os.linesep)
    tree.program=True
    print('semantic_check:')
    try:
        scope = semantic.get_default_scope()
        tree.semantic_check(scope)
        print(*tree.tree, sep=os.linesep)

        with open("llvm.ll", 'w') as f:
            gen = CodeGenerator()
            gen.start()
            tree.to_llvm(gen)
            f.write(str(gen))

    except semantic.SemanticException as e:
        print('Ошибка: {}'.format(e.message))

