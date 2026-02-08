# Arquitetura do Compilador Nativo ULX

O compilador ULX será desenvolvido em C, visando a geração de binários ELF estaticamente linkados que interagem **diretamente com o Kernel Linux via syscalls**, sem depender de bibliotecas de tempo de execução (runtimes) ou bibliotecas padrão (como a glibc). O objetivo é criar uma linguagem de programação verdadeiramente nativa, que **cria sua própria base** de interação com o sistema, definindo sua própria forma de se comportar e eliminando qualquer intermediário desnecessário.

## 1. Princípios Fundamentais

- **Compilação Estática:** Todos os programas ULX serão compilados em binários ELF estáticos, eliminando dependências de bibliotecas dinâmicas e garantindo portabilidade entre distribuições Linux.
- **Acesso Direto ao Kernel (ULX-Kernel-Interface - UKI):** A linguagem fornecerá abstrações de alto nível que se traduzirão diretamente em chamadas de sistema (syscalls) do Linux, **sem depender de bibliotecas padrão como a glibc**. O ULX criará sua própria interface de baixo nível com o kernel, garantindo controle total e máxima performance.
- **Gerenciamento de Memória Próprio:** O ULX implementará seu próprio sistema de alocação e gerenciamento de memória, otimizado para a estrutura e o comportamento dos programas ULX.
- **Abstração de Hardware Customizada:** Para funcionalidades como gráficos, áudio e rede, o ULX desenvolverá suas próprias abstrações de baixo nível, garantindo performance e controle sem depender de APIs de terceiros que possam variar entre distribuições.
- **Auto-Hospedagem (Futura):** O compilador ULX será inicialmente escrito em C, mas o objetivo de longo prazo é que ele possa ser reescrito em ULX, tornando-o auto-hospedado.
- **Sintaxe Simples:** A sintaxe será projetada para ser intuitiva e fácil de aprender, inspirada em linguagens modernas, mas com o poder de controle de baixo nível.

## 2. Componentes do Compilador

### A. Lexer (Analisador Léxico)
- Responsável por transformar o código fonte ULX em uma sequência de tokens (palavras-chave, identificadores, operadores, etc.).

### B. Parser (Analisador Sintático)
- Constrói uma Árvore de Sintaxe Abstrata (AST) a partir dos tokens, verificando a gramática da linguagem.

### C. Semantic Analyzer (Analisador Semântico)
- Realiza verificações de tipo, escopo e outras regras semânticas para garantir a validade do programa.

### D. Code Generator (Gerador de Código)
- Traduz a AST em código de máquina (Assembly) específico para a arquitetura alvo (x86-64, ARM, etc.).

### E. Assembler & Linker (Montador e Ligador)
- O montador converte o código Assembly em código de máquina binário.
- O ligador combina os módulos de código e as bibliotecas estáticas (ULX Standard Library) em um único executável ELF.

## 3. ULX Standard Library (USL)

Uma biblioteca padrão mínima, também escrita em C (e futuramente em ULX), que fornecerá funções básicas para:
- Entrada/Saída (I/O) via syscalls.
- Gerenciamento de memória.
- Operações de string e matemática.
- Funções para interação com o sistema de arquivos.

Esta biblioteca será estaticamente linkada em todos os binários ULX, garantindo que não haja dependências externas em tempo de execução.

## 4. Formato de Pacote `.ulx`

O formato `.ulx` será um arquivo binário auto-executável que contém:
- O binário ELF estático do programa ULX.
- Metadados (nome, versão, ícone, descrição).
- Um pequeno *stub* de instalação que, ao ser executado, integra o programa ao sistema (cria atalho no menu, copia para `/opt`, etc.).

## 5. Ferramentas

- **`ulxc`**: O compilador principal (ULX Compiler).
- **`ulx-pkg`**: Ferramenta para criar e gerenciar pacotes `.ulx`.
- **`ulx-installer`**: O programa gráfico para instalar pacotes `.ulx` com um clique.
