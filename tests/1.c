
int plus(int a, int b){
    return a + b;
}

char[] give_me_ascii(){
    char ascii[128];
    for (int i = 1; i < 128; i = i + 1){
        ascii[i-1] = i;
    }
    return ascii;
}

void main() {

    int a = 1;
    int b = 1;
    int d = 4.1 & 4;

    for (int i = 4; i > 0; i = i - 1) {
        for (int j = 3; j > 0; j = j - 1) {
            print_int(plus(i,j));
        }
    }

    print_string(give_me_ascii());

    char ch = "c";
}


