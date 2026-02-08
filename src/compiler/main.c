#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Uso: ulxc <arquivo.ulx>\n");
        return 1;
    }

    printf("Compilador ULX (Universal Linux eXecution) - Versão 0.1\n");
    printf("Compilando arquivo: %s\n", argv[1]);

    // Aqui virá a lógica de parsing, análise semântica e geração de código de máquina
    // Por enquanto, apenas um placeholder.

    printf("Compilação de %s concluída (placeholder).\n", argv[1]);

    return 0;
}
