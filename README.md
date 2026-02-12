# ULX - Universal Linux eXecution

## A Linguagem de Programação Universal para Linux

ULX é uma linguagem de programação revolucionária projetada para tornar o desenvolvimento de aplicativos para Linux extremamente fácil, rápido e poderoso.

## 🎯 Visão

Transformar cada usuário de Linux em um criador. Queremos que criar um aplicativo seja tão fácil quanto escrever um bilhete, e que compartilhar esse app seja tão simples quanto enviar um arquivo.

## 🏗️ Arquitetura

ULX é composta por três camadas principais:

```
┌─────────────────────────────────────────────────────────────┐
│                        ULX (Linguagem)                       │
│              Sintaxe simples e intuitiva em português        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        CLX (Compilador)                      │
│         Compilador inteligente com IR próprio (SSA)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        LNX (Runtime)                         │
│    Syscalls diretas do Linux - sem dependências de libc      │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Características

- **Sintaxe em Português**: `se`, `senao`, `enquanto`, `para`, `funcao`, `retorne`
- **Syscalls Diretas**: Comunicação direta com o kernel Linux
- **Zero Dependências**: Binários standalone que rodam em qualquer Linux
- **Performance Nativa**: Código compilado para x86-64 com otimizações
- **Type Safety**: Sistema de tipos estático com inferência

## 🚀 Instalação

```bash
# Clonar repositório
git clone https://github.com/DragonSCPOFICIAL/ULX.git
cd ULX

# Compilar compilador
make build

# Instalar
sudo make install
```

## 📝 Exemplo de Código

```ulx
// Hello World em ULX
funcao main() {
    escreva("Hello, ULX World!");
    retorne 0;
}
```

```ulx
// Calculadora simples
funcao soma(a: inteiro, b: inteiro): inteiro {
    retorne a + b;
}

funcao main() {
    var x: inteiro = 10;
    var y: inteiro = 20;
    var resultado: inteiro = soma(x, y);
    escreva(resultado);
    retorne 0;
}
```

```ulx
// Fatorial com recursão
funcao fatorial(n: inteiro): inteiro {
    se (n <= 1) {
        retorne 1;
    }
    retorne n * fatorial(n - 1);
}

funcao main() {
    escreva(fatorial(5));  // 120
    retorne 0;
}
```

```ulx
// Manipulação de arquivos
funcao main() {
    var arquivo = abre("/etc/passwd");
    var conteudo = le(arquivo);
    escreva(conteudo);
    fecha(arquivo);
    retorne 0;
}
```

## 🔧 Compilação

```bash
# Compilar arquivo ULX
ulxc arquivo.ulx -o programa

# Ver IR gerado
ulxc arquivo.ulx --emit-ir

# Compilar e executar
ulxc arquivo.ulx --run
```

## 📚 Sintaxe

### Tipos de Dados

| ULX | Descrição | C Equivalente |
|-----|-----------|---------------|
| `inteiro` | Inteiro 32-bit | `int32_t` |
| `real` | Ponto flutuante 64-bit | `double` |
| `texto` | String | `char*` |
| `booleano` | Booleano | `int8_t` |

### Declarações

```ulx
// Variáveis
var x: inteiro = 10;
var y = 20;  // Inferência de tipo

// Constantes
const PI: real = 3.14159;

// Funções
funcao nome(param: tipo): tipo_retorno {
    // corpo
    retorne valor;
}
```

### Controle de Fluxo

```ulx
// Condicional
se (condicao) {
    // código
} senao {
    // código
}

// While
enquanto (condicao) {
    // código
}

// For
para (var i: inteiro = 0; i < 10; i = i + 1) {
    // código
}
```

### Operadores

| Operador | Descrição |
|----------|-----------|
| `+` | Adição |
| `-` | Subtração |
| `*` | Multiplicação |
| `/` | Divisão |
| `%` | Módulo |
| `==` | Igual |
| `!=` | Diferente |
| `<`, `>`, `<=`, `>=` | Comparação |
| `&&` | AND lógico |
| `\|\|` | OR lógico |
| `!` | NOT lógico |

## 🏛️ Arquitetura do Compilador

```
Código Fonte ULX
       │
       ▼
┌─────────────┐
│    Lexer    │  → Tokens
└─────────────┘
       │
       ▼
┌─────────────┐
│   Parser    │  → AST
└─────────────┘
       │
       ▼
┌─────────────┐
│ Type Checker│  → AST tipada
└─────────────┘
       │
       ▼
┌─────────────┐
│  AST to IR  │  → ULX-IR (SSA)
└─────────────┘
       │
       ▼
┌─────────────┐
│   CodeGen   │  → Assembly x86-64
└─────────────┘
       │
       ▼
┌─────────────┐
│    Linker   │  → ELF64
└─────────────┘
       │
       ▼
   Binário
```

## 🔬 ULX-IR

ULX-IR é a representação intermediária em forma SSA (Static Single Assignment):

```llvm
; Exemplo de IR
define i32 @main() {
entry:
    %x = alloca i32
    store i32 42, i32* %x
    %0 = load i32, i32* %x
    %1 = add i32 %0, 10
    ret i32 %1
}
```

## 🐧 Syscalls Diretas

ULX usa syscalls diretas do Linux sem passar pela libc:

```asm
; sys_write(fd=1, buf=msg, count=len)
mov rax, 1      ; __NR_write
mov rdi, 1      ; stdout
mov rsi, msg    ; buffer
mov rdx, len    ; count
syscall
```

## 📁 Estrutura do Projeto

```
ULX/
├── src/
│   └── compiler/
│       ├── ulxc.py           # Compilador principal
│       ├── ulx_parser.py     # Parser
│       ├── ulx_ir.py         # IR e Builder
│       ├── ulx_codegen.py    # Gerador de código
│       └── elf_generator.py  # Gerador ELF
├── core/
│   └── lnx/
│       ├── lnx_syscall.asm   # Syscalls em assembly
│       └── lnx_syscall.h     # Header C
├── examples/                  # Exemplos ULX
├── docs/                      # Documentação
└── tests/                     # Testes
```

## 🧪 Testes

```bash
# Rodar todos os testes
make test

# Testar exemplo específico
ulxc examples/hello_world.ulx --run
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📜 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Linux Kernel Community
- LLVM Project
- Rust Compiler Team

---

**ULX** - *Linux é de todos. Sem frescura, apenas criação.*
