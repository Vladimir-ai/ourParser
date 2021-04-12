import parser_base
import os

def working_test(debug=False) -> bool:
    string = open('tests/working_test.c', 'r').read()
    # print(parser_base.parse(string).tree())

    try:
        if debug:
            print(*parser_base.parse(string, debug).tree, sep=os.linesep)
        else:
            parser_base.parse(string).tree
        return True
    except:
        return False
