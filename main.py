import parser_base
import os

if __name__ == '__main__':
    print(parser_base.create_parser().parse(
        '''
            a = 1 + b
            
        '''))
    # prog = parser_base.parse('''
    #         int a = 1 + 1
    #         double b = a
    #         bool k = 1
    #         if ( a && b ){
    #             f = 100 / 2
    #         }else{
    #             wdaw = 1
    #             dwawd = 2
    #         }
    #         while (a - b) {
    #             //hhjh
    #         }
    #     ''')
    # print(prog)
    # #print(*prog.tree, sep=os.linesep)