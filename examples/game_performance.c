#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#pragma GCC optimize("O3")
#pragma GCC optimize("inline")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("avx2")

int main() {
    int x = 0;
    int y = 0;
    int vx = 1;
    int vy = 1;
    x = x + vx;
    y = y + vy;
    if (x > 800) {
        vx = -1;
    }
    if (x < 0) {
        vx = 1;
    }
    if (y > 600) {
        vy = -1;
    }
    if (y < 0) {
        vy = 1;
    }
}
printf("Posição final: x=%d\n", x + " y=" + y);
puts("Game rodando com performance extrema!");
    return 0;
}