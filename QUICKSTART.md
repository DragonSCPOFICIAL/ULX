# 🚀 Início Rápido com ULX Studio

Bem-vindo ao futuro do desenvolvimento nativo no Linux! O **ULX Studio** é a sua ferramenta central para criar aplicativos e jogos universais sem a necessidade de comandos complexos.

## 1. Instalação
Se você já clonou o repositório ou baixou o ZIP, instale a base:
```bash
sudo ./install.sh
```

## 2. O Fim do Terminal
Após a instalação, o ULX está integrado ao seu sistema. Você pode:
- **Abrir o Studio:** Procure por "ULX Studio" no seu menu de aplicativos.
- **Instalar Apps:** Dê dois cliques em qualquer arquivo `.ulx` para abrir o instalador visual.

## 3. Criando seu primeiro App Visual
1. Abra o **ULX Studio**.
2. Use o **Editor Visual (Drag & Drop)** para desenhar sua interface.
3. O Studio gerará o código nativo usando a **Dragon-Engine**:
   ```ulx
   func main() {
       ulx_init("Meu App Nativo", 800, 600)
       ui_label("Criado sem Terminal!", {100, 100}, 20)
       ulx_render()
   }
   ```
4. Clique em **"Compilar e Empacotar"**.

## 4. Distribuição Universal
O arquivo `.ulx` gerado é um binário estático. Ele contém o ícone e o código. Envie para qualquer usuário Linux e ele funcionará instantaneamente com um clique duplo!

---
**Dica:** Explore a pasta `examples/` para ver como criar jogos com física e colisão usando a `Dragon-Engine v2`.
