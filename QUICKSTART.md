# 🚀 Início Rápido com ULX Studio

Bem-vindo ao futuro do desenvolvimento nativo no Linux! O **ULX Studio** é a sua ferramenta central para criar aplicativos e jogos universais.

## 1. Instalação
Se você já clonou o repositório, basta rodar:
```bash
sudo ./install.sh
```

## 2. Abrindo o Studio
Você pode abrir o Studio pelo menu de aplicativos do seu Linux ou pelo terminal:
```bash
ulx-studio
```

## 3. Criando seu primeiro App
1. Abra o **ULX Studio**.
2. Selecione **"Novo Projeto"**.
3. Escreva seu código usando a **Dragon-Engine**:
   ```ulx
   func main() {
       ui_window("Meu App", 800, 600)
       ui_text("Olá Mundo Nativo!")
       dragon_run()
   }
   ```
4. Clique em **"Compilar e Empacotar"**.

## 4. Distribuindo
O Studio vai gerar um arquivo `.ulx`. Você pode enviar esse arquivo para qualquer pessoa que tenha a base ULX instalada, e ele funcionará instantaneamente com ícone e performance nativa!

---
**Dica:** Confira a pasta `examples/` para ver modelos prontos de jogos e ferramentas.
