#ifndef EASY_UI_H
#define EASY_UI_H

/* 
 * ULX Easy-UI: A forma mais fácil do mundo de criar apps nativos.
 * Focada em expansão exponencial e simplicidade absoluta.
 */

typedef struct {
    char* titulo;
    int largura;
    int altura;
    char* icone_path;
} ulx_app_t;

// Cria um novo aplicativo com um comando simples
void ulx_criar_app(char* nome, char* icone);

// Adiciona um botão ou elemento visual
void ulx_adicionar_botao(char* texto, void (*acao)());

// Inicia o programa visual
void ulx_rodar();

#endif
