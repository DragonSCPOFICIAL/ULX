#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 
 * ULX Native UI Engine (Baseada em X11)
 * Objetivo: Criar janelas e interfaces sem depender de Python ou bibliotecas pesadas.
 */

void ulx_create_window(char* title, int width, int height) {
    Display *display;
    Window window;
    XEvent event;
    int screen;

    display = XOpenDisplay(NULL);
    if (display == NULL) {
        fprintf(stderr, "Erro: Não foi possível abrir o display X11\n");
        return;
    }

    screen = DefaultScreen(display);
    window = XCreateSimpleWindow(display, RootWindow(display, screen), 10, 10, width, height, 1,
                                 BlackPixel(display, screen), WhitePixel(display, screen));

    XSelectInput(display, window, ExposureMask | KeyPressMask);
    XStoreName(display, window, title);
    XMapWindow(display, window);

    printf("[ULX-NATIVE] Janela '%s' criada com sucesso via X11.\n", title);

    // Loop básico de eventos (apenas para teste inicial)
    /*
    while (1) {
        XNextEvent(display, &event);
        if (event.type == Expose) {
            // Desenhar aqui
        }
        if (event.type == KeyPress)
            break;
    }
    XCloseDisplay(display);
    */
}
