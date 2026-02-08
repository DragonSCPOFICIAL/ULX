#ifndef DRAGON_ENGINE_V2_H
#define DRAGON_ENGINE_V2_H

/* 
 * Dragon-Engine v2: Expansão Exponencial
 * Focada em criação visual de Apps e Jogos sem complexidade.
 */

// --- Estruturas de Dados ---
typedef struct { int x, y; } Vector2;
typedef struct { float r, g, b, a; } Color;

// --- Módulo de Janela e Sistema ---
void ulx_init(char* title, int width, int height);
void ulx_set_background(Color color);
int  ulx_is_running();

// --- Módulo de Interface (Apps) ---
void ui_label(char* text, Vector2 pos, int size);
int  ui_button_clicked(char* label, Vector2 pos, Vector2 size);
void ui_input_field(char* buffer, int max_len, Vector2 pos);

// --- Módulo de Jogos (Games) ---
void game_sprite_create(char* id, char* path);
void game_sprite_move(char* id, Vector2 delta);
int  game_check_collision(char* id1, char* id2);
void game_set_gravity(float value);

// --- Entrada de Usuário ---
int  input_key_pressed(int key_code);
Vector2 input_mouse_pos();

// --- Finalização ---
void ulx_render();
void ulx_close();

#endif
