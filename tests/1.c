
void bubbleSort(int arr[0], int n)
{
   int i, j;
   for (i = 0; i < n-1; i = i + 1) {
   for (j = 0; j < n-i-1; j = j + 1) {
           if (arr[j] > arr[j+1]) {
           int tmp = arr[j];
           arr[j] = arr[j+1];
           arr[j+1] = tmp;
           }
   }
   }

}

char[] give_me_ascii(){
    char ascii[128];
    for (int i = 1; i < 128; i = i + 1){
        ascii[i-1] = i;
    }
    return ascii;
}

void main() {

    int n = 10;

    int a[10];


    for (int i = n; i > 0; i = i - 1) {
        a[n-i] = i;

    }

    for (int i = 0; i < n; i = i + 1) {
    print_int(a[i]);
    }

    bubbleSort(a, n);

    for (int i = 0; i < n; i = i + 1) {
    print_int(a[i]);
    }

    char ch = "c";
}


