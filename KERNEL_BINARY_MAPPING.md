# 🗺️ Mapeamento de Padrões Binários do Kernel para LNX, ULX e CLX

Com base na análise aprofundada do código-fonte do Kernel Linux, definimos como cada componente do ecossistema ULX se integrará nativamente ao sistema, garantindo performance e controle sem precedentes.

## 1. LNX: Acesso Direto ao Coração do Hardware

A camada **LNX** será a interface de baixíssimo nível, atuando como uma extensão do próprio Kernel. Ela utilizará os seguintes padrões binários:

-   **Syscalls Diretas (x86_64 ABI):** O LNX fará chamadas de sistema (`syscall`) diretamente, sem a intermediação da `libc`. Isso significa que o LNX manipulará os registradores (`%rax`, `%rdi`, `%rsi`, `%rdx`, etc.) exatamente como o Kernel espera, garantindo a comunicação mais rápida possível com o sistema [1].
-   **Inicialização Precoce (inspirado em `start_kernel()`):** O LNX será projetado para se integrar no processo de boot do sistema, permitindo que ele configure o hardware de projeção holográfica e outros periféricos antes mesmo que o ambiente gráfico tradicional seja carregado. Isso garante que a "janela holográfica" seja uma funcionalidade intrínseca do sistema, não um aplicativo de usuário.
-   **Controle de Framebuffer e I/O de Hardware:** Para a projeção holográfica, o LNX acessará diretamente os buffers de memória de vídeo (como os drivers de framebuffer do Linux) e portas de I/O de hardware. Isso permite a manipulação de pixels e feixes de luz em um nível binário, essencial para criar a percepção de profundidade e realidade da holografia.

## 2. ULX: Abstração Humana para o Poder Binário

A linguagem **ULX** será a camada de programação de alto nível, focada na simplicidade e na experiência do desenvolvedor. Ela abstrairá a complexidade binária do LNX da seguinte forma:

-   **Comandos Intuitivos:** Funções como `ProjetarJanela()` ou `MostrarTexto()` no ULX serão traduzidas pelo CLX para sequências de syscalls e operações de hardware do LNX. O desenvolvedor não precisará se preocupar com registradores ou endereços de memória.
-   **Tipagem Forte e Segura:** Embora o LNX opere em um nível binário, o ULX fornecerá um sistema de tipos robusto para evitar erros comuns de programação de baixo nível, garantindo que as operações de hardware sejam seguras e previsíveis.
-   **Gerenciamento Automático de Recursos:** O ULX cuidará da alocação e desalocação de recursos de hardware e memória, permitindo que o desenvolvedor se concentre na lógica do aplicativo holográfico.

## 3. CLX: O Compilador que Une os Mundos

O **CLX** será o compilador que faz a ponte entre a simplicidade do ULX e o poder binário do LNX. Suas otimizações e geração de código serão diretamente influenciadas pelos padrões do Kernel:

-   **Geração de Binários ELF64 Estáticos:** O CLX produzirá executáveis ELF64 que são totalmente estáticos, ou seja, não dependem de bibliotecas externas como a `libc`. Isso garante que os programas ULX rodem em qualquer distribuição Linux sem problemas de compatibilidade [2].
-   **Injeção de Syscalls Otimizadas:** Ao compilar o código ULX, o CLX identificará as operações que requerem interação com o Kernel e gerará as instruções `syscall` correspondentes, preenchendo os registradores com os argumentos corretos de forma eficiente.
-   **Linkagem com o LNX:** O CLX incluirá o código da base LNX diretamente no binário final, criando um executável monolítico que contém tanto a lógica do aplicativo ULX quanto a interface de hardware do LNX. Isso elimina a necessidade de módulos de kernel separados ou drivers externos para a funcionalidade holográfica.
-   **Ponto de Entrada `_start` Minimalista:** O CLX gerará um ponto de entrada `_start` otimizado que inicializa o ambiente de execução do ULX e chama a função principal do aplicativo, seguido por uma syscall `exit` limpa, espelhando a forma como o Kernel inicia e encerra processos.

---

### Referências

[1] Linux System Call Table for x86 64 · Ryan A. Chapman. Disponível em: [https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)
[2] Writing C software without the standard library [Linux Edition]. Disponível em: [https://gist.github.com/tcoppex/443d1dd45f873d96260195d6431b0989](https://gist.github.com/tcoppex/443d1dd45f873d96260195d6431b0989)
