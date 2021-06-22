from compiler import parser_base, semantic
import os
import compiler.code_generator as msil
import subprocess

from compiler.tests import working_test

if __name__ == '__main__':
    prog = open('tests/1.c', 'r').read()

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
    except semantic.SemanticException as e:
        print('Ошибка: {}'.format(e.message))

    gen = msil.CodeGenerator()
    gen.start()
    tree.msil(gen)
    gen.end()

    file = open('output/1.il', 'w')

    file.write(str(gen))

    print(gen)


