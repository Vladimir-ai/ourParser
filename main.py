import parser_base
import os

if __name__ == '__main__':
    prog = '''
            /* a = 1 + b;
            if (a < 2){
                d = b;
            }
            if (a > 2){
                w = w;
            }else{
                _A = 1;
            }
            
            if (a == 2) a = 3;
            else b = 5;
            
            while (b < 0)
             b = b + 1;
            while (b < 0){
                index = 1;
                b = b+1;
            }
            
            for (int a = 0; a < 2; a = a + 2){
                d = 0;
                d = 1;
            }
            
            for (int a = 0; a < 2; a = a + 2) d = d + 1;
            f = 2.9 + 1e4;
            //int b = 1 % 2;
        
            for (;;);
            
            return a = 0; 
            */
//            if (1 < 2); //WARNING!!! it's not call!!!
            while (1 < 2);
            while(a);
            //int b = 2;
    
        '''
    print(*parser_base.parse(prog, True).tree, sep=os.linesep)
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