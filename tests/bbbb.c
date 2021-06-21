int fib(int num){

    if (num <= 1)
        return num;

    return fib(num - 1) + fib(num - 2);

}

int main(){

    int a[10];
    int b[10];

    b[1] = 10;
    a[1] = 2;

    b = a;

    print_int(b[1]);

    a[1] = 1;
    print_int(b[1]);

//    float c[3];
//
//    c[1] = 2;

//    float d[5];
//    d[10] = 5;
//
//    d = c;

//    int b = c[1];
//    int a = 0;
//    int b = -1;
//    c[1] = 10;
//    c[-1] = 20;
//    int f = c[1];

//
//
//    a = b + -1;
//
//   // float b = read_float();
//
//    print_int(c[0]);
//    print_int(d[1]);
//    print_int(f);
//    print_int(c[-1]);
//    print_int(a);
    return 0;
// найти максимальное число фибоначчи не более заданного
//    int a = 1, b = 0;
//    a = (1 + 2) * 2; // 6
//    b = a / 2; // 3
//
//    a = 1 + -1;
//
//    float d = 2.1;
//    int i;
//    for (i = 110 ; i < 121; i = i + 1){
//        print_char(i);
//        print_int(f);

//    }
//
//    print_int(b); //3
//    b = b == 3;
//
//    print_int(b); //1
//    print_int(1 + 1); //1
//    print_float(d);
}