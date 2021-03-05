import parser_base
import os

if __name__ == '__main__':
    print(parser_base.create_parser().parse(
        '''/*
            a = 1 + b
            if (a < 2){
                d = b
            }
            if (a > 2){
                w = w
            }else{
                _A = 1
            }
            
            if (a == 2) a = 3;
            else b = 5;
            
            while (b < 0) b = b + 1;
            while (b < 0){
                index = 1;
                b = b+1;
            }*/
            
            for (int a = 0; a < 2; a = a + 2){
                d = 0;
                d = 1;
            }
            
            for (int a = 0; a < 2; a = a + 2) d = d + 1;
            
            
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