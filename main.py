import parser_base
import os

if __name__ == '__main__':
    prog = parser_base.parse('''
            int a = 1 + 1
            double b = a
            bool k = 1
            if ( a && b ){
                f = 100 / 2
            }else{
                wdaw = 1
                dwawd = 2
            }
            while (a - b) {
                //hhjh
            }
        ''')
    print(prog)
    #print(*prog.tree, sep=os.linesep)