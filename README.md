# ULX (Universal Linux eXecution)

> "A linguagem de programação nativa e universal para Linux. Compilação estática, zero dependências, máxima performance."

O **ULX** é um projeto ambicioso que visa criar uma linguagem de programação de baixo nível, compilada estaticamente para binários ELF, que interage diretamente com o Kernel Linux via syscalls. Nosso objetivo é eliminar a fragmentação de dependências entre distribuições e fornecer uma ferramenta poderosa para o desenvolvimento de aplicações e jogos verdadeiramente nativos para o ecossistema Linux.

## 🚀 Filosofia ULX

- **Nativo por Design:** O compilador ULX é escrito em C e gera código de máquina puro, sem a necessidade de runtimes ou interpretadores externos.
- **Universalidade:** Programas ULX são compilados estaticamente, garantindo que rodem em qualquer distribuição Linux (Arch, Ubuntu, Fedora, etc.) sem problemas de dependência.
- **Performance Extrema:** Acesso direto ao Kernel e otimização para hardware Linux, resultando em aplicações ultra-rápidas.
- **Simplicidade:** Sintaxe intuitiva e poderosa, focada em produtividade e controle.

## 🛠️ Componentes Principais

- **`ulxc` (ULX Compiler):** O compilador principal, responsável por transformar o código fonte ULX em binários ELF estáticos.
- **ULX Standard Library (USL):** Uma biblioteca mínima e estaticamente linkada que fornece funcionalidades básicas de I/O, memória e sistema.
- **Formato de Pacote `.ulx`:** Um formato de arquivo binário auto-executável para distribuição e instalação de aplicações ULX.
- **`ulx-installer`:** Uma ferramenta gráfica para instalação "one-click" de pacotes `.ulx`.

## ⚙️ Instalação Rápida (Universal)

Se você não tem o GitHub CLI (`gh`) configurado, use o método via `curl` que funciona em qualquer distro:

```bash
curl -L https://github.com/DragonSCPOFICIAL/ULX/archive/refs/heads/main.zip -o ulx.zip
# Se não tiver o unzip: sudo pacman -S unzip (Arch) ou sudo apt install unzip (Ubuntu)
unzip ulx.zip
cd ULX-main
sudo ./install.sh
```

## 🏗️ Estrutura do Projeto

- `/src/compiler`: Código fonte do compilador ULX (escrito em C).
- `/src/lib`: Código fonte da ULX Standard Library (USL).
- `/bin`: Binários compilados (ulxc, ulx-pkg, ulx-installer).
- `/examples`: Exemplos de código ULX.
- `/docs`: Documentação técnica e especificações.
- `/sdk`: Ferramentas e bibliotecas para desenvolvedores ULX.

---

**Junte-se a nós na construção da próxima geração de software nativo para Linux!**
