#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#pragma GCC optimize("O3")
#pragma GCC optimize("inline")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("avx2")

int main() {
    int i = 1; for (i = 1; i <= 10; i = i + 1) {
        printf("%d\n", i);
    }
    return 0;
}