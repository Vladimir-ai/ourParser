int print_arr(char arr[10], int n){
    for(int i = 0; i < n; i = i + 1){
        print_char(arr[i]);
    }
    return 0;
}

int main(){

    char a[10];
    int b[20];
//    a[1] = aaaaa(1);

    int n = 10;
    int k = 0;

    int c = 0;
    float g = c;
    bool cc = 0;
    float gg = cc;
    char ccc = "a";
    float ggg = ccc;

    print_float(g);
    print_float(gg);
    print_float(ggg);

    a = read_str();

    char arr[10];

    arr = a;

    for (int i = 0; i < n - 1; i = i + 1)
        for (int j = 0; j < n - i - 1; j = j + 1){
            int ind = j + 1;
            if (arr[j] < arr[j + 1]){
                int temp = arr[ind];
                arr[j + 1] = arr[j];
                arr[j] = temp;
            }
        }

    print_arr(arr, 10);

//    for (k = 0; k < n; k = k + 1){
//        print_char(arr[k]);
//    }

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