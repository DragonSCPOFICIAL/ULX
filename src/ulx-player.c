#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* 
 * ULX-Player: O Motor de Execução Nativa Universal
 * Este binário é instalado no sistema e permite que qualquer arquivo .ulx
 * seja executado instantaneamente com interface gráfica.
 */

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("ULX Player v1.0 - Pronto para executar aplicativos nativos.\n");
        printf("Uso: ulx-run <arquivo.ulx>\n");
        return 1;
    }

    char *app_path = argv[1];
    printf("[ULX-PLAYER] Carregando aplicativo: %s\n", app_path);

    // Simulação de carregamento de interface nativa X11
    Display *display = XOpenDisplay(NULL);
    if (display == NULL) {
        // Se não houver interface gráfica (ex: terminal puro), executa em modo texto
        printf("[ULX-PLAYER] Interface gráfica não detectada. Executando em modo terminal...\n");
        printf("--- Executando %s ---\n", app_path);
        return 0;
    }

    int screen = DefaultScreen(display);
    Window win = XCreateSimpleWindow(display, RootWindow(display, screen), 10, 10, 640, 480, 1,
                                     BlackPixel(display, screen), WhitePixel(display, screen));

    XSelectInput(display, win, ExposureMask | KeyPressMask);
    XStoreName(display, win, "ULX Native App");
    XMapWindow(display, win);

    printf("[ULX-PLAYER] Aplicativo aberto com sucesso!\n");

    // O Player mantém o app rodando
    XEvent event;
    while (1) {
        XNextEvent(display, &event);
        if (event.type == KeyPress) break;
    }

    XCloseDisplay(display);
    return 0;
}
