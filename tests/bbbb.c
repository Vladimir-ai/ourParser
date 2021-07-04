void print_arr(char arr[10], int n){
    for(int i = 0; i < n; i = i + 1){
        print_char(arr[i]);
    }
    return;
}

void sortAndPrint(char arr[10], int n){
    for (int i = 0; i < n - 1; i = i + 1)
        for (int j = 0; j < n - i - 1; j = j + 1)
            if (arr[j] < arr[j + 1]){
                int temp = arr[j + 1];
                arr[j + 1] = arr[j];
                arr[j] = temp;
            }

    print_arr(arr, n);
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

    print_char("b");
    for (int i = 0; i < 10; i = i + 1){
        print_int(i);
    }

    print_char("a");
    for (int i = 10; i >= 0; i = i - 1)
        print_int(i);

    char arr[10];

    arr = a;

    sortAndPrint(arr, 10);

    return 0;
}