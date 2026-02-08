#ifndef DRAGON_ENGINE_H
#define DRAGON_ENGINE_H

/* 
 * Dragon-Engine: O motor universal do ULX para Apps e Jogos.
 * Simplicidade absoluta para criação nativa.
 */

// --- Módulo de Aplicativo (UI) ---
void ui_window(char* title, int w, int h);
void ui_button(char* label, void (*callback)());
void ui_text(char* content);

// --- Módulo de Jogo (Game) ---
void game_init();
void game_load_sprite(char* id, char* path);
void game_draw_sprite(char* id, int x, int y);
void game_on_update(void (*update_func)());

// --- Sistema ---
void dragon_run();

#endif
