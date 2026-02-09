/*
 * LNX Native Bridge - Core Library
 * 
 * Esta biblioteca permite que aplicativos ULX sejam executados de forma 100% nativa
 * no Linux, desconectando-os do terminal e integrando-os diretamente ao sistema.
 */

#ifndef LNX_NATIVE_BRIDGE_H
#define LNX_NATIVE_BRIDGE_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>

/**
 * Desconecta o processo atual do terminal de controle.
 * Isso impede que o programa abra um console ou dependa de um.
 */
void lnx_detach_from_console() {
    pid_t pid;

    // Primeiro fork para criar um novo processo
    pid = fork();

    if (pid < 0) exit(EXIT_FAILURE);
    if (pid > 0) exit(EXIT_SUCCESS); // O pai morre, o filho continua

    // Torna o filho o líder da sessão
    if (setsid() < 0) exit(EXIT_FAILURE);

    // Segundo fork para garantir que o processo não possa adquirir um terminal novamente
    pid = fork();

    if (pid < 0) exit(EXIT_FAILURE);
    if (pid > 0) exit(EXIT_SUCCESS);

    // Define permissões de arquivo padrão
    umask(0);

    // Muda para o diretório raiz para não travar montagens de disco
    chdir("/");

    // Fecha os descritores de arquivo padrão (stdin, stdout, stderr)
    // Isso é o que realmente "mata" a dependência do console
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

    // Redireciona para /dev/null para evitar erros de escrita
    open("/dev/null", O_RDONLY); // stdin
    open("/dev/null", O_WRONLY); // stdout
    open("/dev/null", O_RDWR);   // stderr
}

/**
 * Registra o aplicativo no sistema Linux (.desktop)
 */
void lnx_register_app(const char* name, const char* exec_path, const char* icon_path) {
    char desktop_file[1024];
    sprintf(desktop_file, "%s/.local/share/applications/%s.desktop", getenv("HOME"), name);
    
    FILE *f = fopen(desktop_file, "w");
    if (f) {
        fprintf(f, "[Desktop Entry]\n");
        fprintf(f, "Type=Application\n");
        fprintf(f, "Name=%s\n", name);
        fprintf(f, "Exec=%s\n", exec_path);
        fprintf(f, "Icon=%s\n", icon_path ? icon_path : "system-run");
        fprintf(f, "Terminal=false\n"); // AQUI ESTÁ O SEGREDO
        fprintf(f, "Categories=Utility;Development;\n");
        fclose(f);
    }
}

#endif
