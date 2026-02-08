# ULX (Universal Linux eXecution)

> "A linguagem de programação nativa e universal para Linux. Compilação estática, zero dependências, máxima performance."

O **ULX** é um projeto ambicioso que visa criar uma linguagem de programação de baixo nível, compilada estaticamente para binários ELF, que interage diretamente com o Kernel Linux via syscalls. Nosso objetivo é eliminar a fragmentação de dependências entre distribuições e fornecer uma ferramenta poderosa para o desenvolvimento de aplicações e jogos verdadeiramente nativos para o ecossistema Linux.

## 🚀 Filosofia ULX

- **Independência Total (Zero Python):** O ecossistema ULX está sendo migrado para C puro e X11 nativo. O objetivo é eliminar qualquer dependência de interpretadores externos.
- **UI Nativa (Dragon-Engine):** Criação de janelas e interfaces gráficas falando diretamente com o servidor de vídeo (X11/Wayland), garantindo performance máxima e baixo consumo de memória.
- **Compilação Estática Universal:** Binários que carregam tudo o que precisam, garantindo que um programa compilado no Arch rode no Ubuntu sem erros de biblioteca.
- **Performance Extrema:** Acesso direto ao Kernel e otimização para hardware Linux, resultando em aplicações ultra-rápidas.

## 🛠️ Componentes Principais

- **`ulxc` (ULX Compiler):** O compilador principal, responsável por transformar o código fonte ULX em binários ELF estáticos.
- **`ulx-studio`:** IDE nativa para desenvolvimento visual de apps e jogos.
- **Formato de Pacote `.ulx`:** Um formato de arquivo binário auto-executável para distribuição e instalação de aplicações ULX.
- **`ulx-handler`:** Integrador de sistema que permite a execução e instalação visual de pacotes `.ulx`.

## ⚙️ Instalação Rápida (Universal)

Se você não tem o GitHub CLI (`gh`) configurado, use o método via `curl` que funciona em qualquer distro:

```bash
# 1. Baixar e extrair
curl -L https://github.com/DragonSCPOFICIAL/ULX/archive/refs/heads/main.zip -o ulx.zip
unzip ulx.zip && cd ULX-main

# 2. Instalar dependências de sistema (X11 para UI Nativa)
# No Arch: sudo pacman -S libx11 gcc make unzip
# No Ubuntu: sudo apt install libx11-dev gcc make unzip

# 3. Instalar Ecossistema ULX
sudo ./install.sh
```

## 🏗️ Estrutura do Projeto

- `/src/compiler`: Código fonte do compilador ULX (escrito em C).
- `/src/lib`: Bibliotecas nativas (UI X11, USL).
- `/bin`: Binários compilados (ulxc, ulx-studio, ulx-pack).
- `/examples`: Exemplos de código ULX e modelos de projetos.
- `/include`: Cabeçalhos da Dragon-Engine para desenvolvedores.

---

**Junte-se a nós na construção da próxima geração de software nativo para Linux!**
