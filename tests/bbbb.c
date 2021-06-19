int aa(int a, int b){
    print_int(a);
    print_int(b);
    if (a + b < 10){
        return aa(a + 1, b + 1);
    }
    return a;
}

int main(){

    float b = read_float();

//    print_int(aa(1,1));
    print_float(b);
    return 0;
// найти максимальное число фибоначчи не более заданного
//    int a = 1, b = 0;
//    a = (1 + 2) * 2; // 6
//    b = a / 2; // 3
//
//    a = 1 + -1;
//
//    float d = 2.1;
//    for (int i = 0; i < 121; i = i + 1){
//        print_char(i);
//    }
//
//    print_int(b); //3
//    b = b == 3;
//
//    print_int(b); //1
//    print_int(1 + 1); //1
//    print_float(d);
}