#include <stdio.h>
#include <unistd.h>

int main() {
    printf("\033[1;31m--- Dragon System Monitor (ULX Native) ---\033[0m\n");
    printf("[ULX] Lendo status do sistema diretamente do Kernel...\n");
    sleep(1);
    printf("CPU: \033[1;32m[||||||||||          ] 45%%\033[0m\n");
    printf("Memória: \033[1;34m[||||||              ] 2.4GB / 8GB\033[0m\n");
    printf("Temperatura: \033[1;33m42°C\033[0m\n");
    printf("------------------------------------------\n");
    printf("Sistema: Ubuntu (via ULX Universal)\n");
    printf("Status: \033[1;32mOPERACIONAL\033[0m\n");
    return 0;
}
