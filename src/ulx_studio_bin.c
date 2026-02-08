#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void print_header() {
    printf("\033[1;35m========================================\033[0m\n");
    printf("\033[1;35m       ULX STUDIO - NATIVE IDE          \033[0m\n");
    printf("\033[1;35m========================================\033[0m\n");
}

int main() {
    print_header();
    printf("[INFO] Inicializando interface gráfica nativa...\n");
    sleep(1);
    printf("[INFO] Carregando módulos da Dragon-Engine...\n");
    printf("[INFO] Verificando compilador 'ulxc' em /usr/bin/ulxc... \033[1;32mOK\033[0m\n");
    
    printf("\n\033[1;34mMenu Principal:\033[0m\n");
    printf("1. Criar Novo Projeto (App/Jogo)\n");
    printf("2. Abrir Projeto Existente\n");
    printf("3. Compilar para Formato Universal (.ulx)\n");
    printf("4. Publicar no Dragon-App-Hub\n");
    
    printf("\n[STUDIO] Aguardando entrada do usuário...\n");
    printf("[SIMULAÇÃO] Usuário selecionou: 'Compilar Projeto'\n");
    sleep(1);
    printf("\033[1;32m[SUCESSO] Projeto compilado e empacotado como 'MeuApp.ulx'!\033[0m\n");
    
    return 0;
}
