#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int a = 10;
    int b = 20;
    int result = (a + (b * 2));
    if ((result >= 40)) {
        printf("%s\n", "Large");
    } else {
        printf("%s\n", "Small");
    }
    int x = 1;
    while ((x <= 3)) {
        printf("%d\n", x);
        x = (x + 1);
    }
    return 0;
}
