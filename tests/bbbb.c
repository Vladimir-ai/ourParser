//int aa(int a, int b, int c[10]){
//    print_int(a);
//    print_int(b);
//    if (a + b < 10){
//        return aa(a + 1, b + 1, c);
//    }
//    return a;
//}

int aa(int c[10]){

    c[1] = 2;
    c[2] = 5;
    c[3] = c[1] + c[2];

    return c[3];
}

int main(){
//    int g = 1 + 0.5;
//    float g = 1.3 + 1;
//    int a = g;
    float g = 5.1;


    int a[10];
    a[1] = 1;
    a[2] = 4;
    a[3] = a[1] + a[2];

    float g[10];

    print_int(a[3]);
    print_int(aa(a));

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