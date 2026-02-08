#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#pragma GCC optimize("O3")
#pragma GCC optimize("inline")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("avx2")

int main() {
    int a = 10;
    int b = 5;
    printf("Soma: %d\n", (a + b));
    printf("Subtração: %d\n", (a - b));
    printf("Multiplicação: %d\n", (a * b));
    printf("Divisão: %d\n", (a / b));
    return 0;
}