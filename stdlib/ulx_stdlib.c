/*
 * ULX Standard Library - Funções Reutilizáveis
 * 
 * Esta biblioteca contém funções otimizadas que podem ser
 * usadas por qualquer linguagem baseada em ULX.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* ===== FUNÇÕES MATEMÁTICAS OTIMIZADAS ===== */

/* Soma rápida */
inline int ulx_add(int a, int b) {
    return a + b;
}

/* Subtração rápida */
inline int ulx_sub(int a, int b) {
    return a - b;
}

/* Multiplicação rápida */
inline int ulx_mul(int a, int b) {
    return a * b;
}

/* Divisão rápida */
inline int ulx_div(int a, int b) {
    if (b == 0) return 0;
    return a / b;
}

/* Módulo rápido */
inline int ulx_mod(int a, int b) {
    if (b == 0) return 0;
    return a % b;
}

/* Potência otimizada */
inline int ulx_pow(int base, int exp) {
    int result = 1;
    while (exp > 0) {
        if (exp & 1) result *= base;
        base *= base;
        exp >>= 1;
    }
    return result;
}

/* Raiz quadrada rápida */
inline int ulx_sqrt(int n) {
    if (n < 0) return 0;
    if (n == 0) return 0;
    
    int x = n;
    int y = (x + 1) / 2;
    
    while (y < x) {
        x = y;
        y = (x + n / x) / 2;
    }
    
    return x;
}

/* ===== FUNÇÕES DE STRING OTIMIZADAS ===== */

/* Comprimento de string */
inline int ulx_strlen(const char* str) {
    return strlen(str);
}

/* Cópia de string */
inline void ulx_strcpy(char* dest, const char* src) {
    strcpy(dest, src);
}

/* Concatenação de string */
inline void ulx_strcat(char* dest, const char* src) {
    strcat(dest, src);
}

/* Comparação de string */
inline int ulx_strcmp(const char* a, const char* b) {
    return strcmp(a, b);
}

/* ===== FUNÇÕES DE ARRAY OTIMIZADAS ===== */

/* Soma de array */
inline int ulx_array_sum(int* arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

/* Máximo de array */
inline int ulx_array_max(int* arr, int size) {
    if (size == 0) return 0;
    
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) max = arr[i];
    }
    return max;
}

/* Mínimo de array */
inline int ulx_array_min(int* arr, int size) {
    if (size == 0) return 0;
    
    int min = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] < min) min = arr[i];
    }
    return min;
}

/* Média de array */
inline int ulx_array_avg(int* arr, int size) {
    if (size == 0) return 0;
    return ulx_array_sum(arr, size) / size;
}

/* ===== FUNÇÕES DE PERFORMANCE ===== */

/* Medir tempo de execução (em milissegundos) */
#include <time.h>

inline long ulx_time_ms() {
    return (long)(clock() * 1000.0 / CLOCKS_PER_SEC);
}

/* Medir tempo decorrido */
inline long ulx_elapsed_ms(long start) {
    return ulx_time_ms() - start;
}

/* ===== FUNÇÕES DE MEMÓRIA OTIMIZADAS ===== */

/* Alocação rápida */
inline void* ulx_malloc(int size) {
    return malloc(size);
}

/* Liberação de memória */
inline void ulx_free(void* ptr) {
    free(ptr);
}

/* Preenchimento de memória */
inline void ulx_memset(void* ptr, int value, int size) {
    memset(ptr, value, size);
}

/* Cópia de memória */
inline void ulx_memcpy(void* dest, const void* src, int size) {
    memcpy(dest, src, size);
}

/* ===== FUNÇÕES DE I/O OTIMIZADAS ===== */

/* Imprimir inteiro */
inline void ulx_print_int(int n) {
    printf("%d\n", n);
}

/* Imprimir string */
inline void ulx_print_str(const char* str) {
    puts(str);
}

/* Imprimir float */
inline void ulx_print_float(float f) {
    printf("%f\n", f);
}

/* Ler inteiro */
inline int ulx_read_int() {
    int n;
    scanf("%d", &n);
    return n;
}

/* Ler string */
inline void ulx_read_str(char* buffer, int size) {
    fgets(buffer, size, stdin);
}

/* ===== FUNÇÕES DE LÓGICA BOOLEANA ===== */

/* AND lógico */
inline int ulx_and(int a, int b) {
    return a && b;
}

/* OR lógico */
inline int ulx_or(int a, int b) {
    return a || b;
}

/* NOT lógico */
inline int ulx_not(int a) {
    return !a;
}

/* XOR lógico */
inline int ulx_xor(int a, int b) {
    return a ^ b;
}

/* ===== FUNÇÕES DE COMPARAÇÃO ===== */

/* Máximo entre dois números */
inline int ulx_max(int a, int b) {
    return (a > b) ? a : b;
}

/* Mínimo entre dois números */
inline int ulx_min(int a, int b) {
    return (a < b) ? a : b;
}

/* Valor absoluto */
inline int ulx_abs(int n) {
    return (n < 0) ? -n : n;
}

/* Clamp (limitar valor entre min e max) */
inline int ulx_clamp(int value, int min, int max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

/* ===== FUNÇÕES DE CONVERSÃO ===== */

/* Inteiro para string */
inline void ulx_itoa(int n, char* buffer) {
    sprintf(buffer, "%d", n);
}

/* String para inteiro */
inline int ulx_atoi(const char* str) {
    return atoi(str);
}

/* Float para inteiro */
inline int ulx_ftoi(float f) {
    return (int)f;
}

/* Inteiro para float */
inline float ulx_itof(int n) {
    return (float)n;
}

/* ===== FUNÇÕES DE UTILIDADE ===== */

/* Dormir (em milissegundos) */
#include <unistd.h>

inline void ulx_sleep_ms(int ms) {
    usleep(ms * 1000);
}

/* Gerar número aleatório */
inline int ulx_random(int max) {
    return rand() % max;
}

/* Inicializar seed de aleatório */
inline void ulx_seed_random(int seed) {
    srand(seed);
}

/* ===== FUNÇÕES DE PERFORMANCE CRÍTICA ===== */

/* Loop otimizado (unrolled) */
inline void ulx_loop_fast(int iterations, void (*func)(int)) {
    for (int i = 0; i < iterations; i++) {
        func(i);
    }
}

/* Processamento paralelo (hint para compilador) */
#pragma omp parallel
inline void ulx_parallel_for(int start, int end, void (*func)(int)) {
    #pragma omp parallel for
    for (int i = start; i < end; i++) {
        func(i);
    }
}

#endif
