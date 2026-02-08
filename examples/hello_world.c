#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#pragma GCC optimize("O3")
#pragma GCC optimize("inline")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("avx2")

int main() {
    puts("Olá, mundo!");
    return 0;
}