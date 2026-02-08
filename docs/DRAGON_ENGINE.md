# 🐉 Dragon-Engine v2: Manual de Referência

A **Dragon-Engine** é o coração gráfico e lógico do ecossistema ULX. Ela foi projetada para ser a biblioteca mais simples e poderosa para criação de software nativo no Linux.

## 🖼️ Módulo de Interface (UI)

### `ulx_init(title, width, height)`
Inicializa a janela do aplicativo.
- **title**: Nome que aparecerá na barra de título.
- **width/height**: Dimensões da janela.

### `ui_label(text, position, size)`
Desenha um texto na tela.
- **position**: Coordenadas `{x, y}`.
- **size**: Tamanho da fonte.

### `ui_button_clicked(label, position, size)`
Cria um botão interativo. Retorna `1` se for clicado.
```ulx
if (ui_button_clicked("Clique Aqui", {100, 100}, {200, 50})) {
    print("Botão pressionado!");
}
```

## 🎮 Módulo de Jogos (Game)

### `game_sprite_create(id, path)`
Carrega uma imagem e a transforma em um objeto de jogo (Sprite).
- **path**: Caminho para o arquivo PNG/JPG (será embutido no .ulx).

### `game_sprite_move(id, delta)`
Move o objeto na tela.
- **delta**: Vetor de movimento `{x, y}`.

### `game_set_gravity(value)`
Ativa a física global do jogo.
- **value**: Força da gravidade (ex: 9.8).

### `game_check_collision(id1, id2)`
Retorna `1` se dois objetos se tocaram.

## ⌨️ Entrada de Usuário

- `input_key_pressed(key_code)`: Verifica se uma tecla está pressionada.
- `input_mouse_pos()`: Retorna a posição atual do mouse.

## 🚀 Ciclo de Vida

- `ulx_render()`: Atualiza a tela e processa eventos.
- `ulx_close()`: Fecha o programa e limpa a memória.
