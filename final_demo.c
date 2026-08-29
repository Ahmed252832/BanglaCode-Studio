#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int marks = 75;
    int bonus = 5;
    int finalMarks = (marks + bonus);
    printf("%s\n", "BanglaCode Demo");
    printf("%d\n", finalMarks);
    if ((finalMarks >= 40)) {
        printf("%s\n", "Pass");
    } else {
        printf("%s\n", "Fail");
    }
    int count = 1;
    while ((count <= 3)) {
        printf("%d\n", count);
        count = (count + 1);
    }
    return 0;
}
