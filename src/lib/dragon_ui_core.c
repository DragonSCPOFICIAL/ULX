#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <stdio.h>
#include <stdlib.h>

/* 
 * Dragon-UI Core
 * Biblioteca nativa do ULX para desenho de janelas e botões.
 */

typedef struct {
    Display *display;
    Window window;
    int screen;
} DragonWindow;

DragonWindow* dragon_ui_init(char* title, int w, int h) {
    DragonWindow* dw = malloc(sizeof(DragonWindow));
    dw->display = XOpenDisplay(NULL);
    if (dw->display == NULL) return NULL;

    dw->screen = DefaultScreen(dw->display);
    dw->window = XCreateSimpleWindow(dw->display, RootWindow(dw->display, dw->screen), 
                                     10, 10, w, h, 1,
                                     BlackPixel(dw->display, dw->screen), 
                                     WhitePixel(dw->display, dw->screen));

    XSelectInput(dw->display, dw->window, ExposureMask | KeyPressMask | ButtonPressMask);
    XStoreName(dw->display, dw->window, title);
    XMapWindow(dw->display, dw->window);

    return dw;
}

void dragon_ui_draw_button(DragonWindow* dw, int x, int y, char* label) {
    GC gc = DefaultGC(dw->display, dw->screen);
    XDrawRectangle(dw->display, dw->window, gc, x, y, 100, 30);
    XDrawString(dw->display, dw->window, gc, x + 20, y + 20, label, strlen(label));
    XFlush(dw->display);
}
