#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma GCC optimize("O3")
#pragma GCC optimize("Ofast")
#pragma GCC target("native")
#pragma omp parallel
#pragma omp simd

int main() {
    puts("Olá, mundo!");
    return 0;
}