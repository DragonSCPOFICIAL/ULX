# Arquitetura de ULX

## Estrutura em Três Camadas

```
┌──────────────────────────────────────────────────────┐
│  ULX - Universal Linux (A Linguagem)                 │
│  ─────────────────────────────────────────────────   │
│  - Sintaxe simples e intuitiva                       │
│  - Fácil de aprender e usar                          │
│  - Abstração de alto nível                           │
│  - Foco no que fazer, não como fazer                 │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│  CLX - Compilador (Traduz ULX para C)                │
│  ─────────────────────────────────────────────────   │
│  - Parse da sintaxe ULX                              │
│  - Análise semântica                                 │
│  - Geração de código C otimizado                     │
│  - Otimizações de compilação                         │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│  LX - Tradutor Hardware (Traduz para assembly)       │
│  ─────────────────────────────────────────────────   │
│  - Acesso direto a syscalls Linux                    │
│  - Tradução para assembly nativo                     │
│  - Otimizações de hardware                           │
│  - Compatibilidade com todas as arquiteturas         │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│  Hardware + Kernel Linux                             │
│  ─────────────────────────────────────────────────   │
│  - CPU (x86-64, ARM, RISC-V, etc)                    │
│  - Kernel Linux (qualquer versão, qualquer distro)   │
│  - Syscalls do sistema                               │
│  - Execução real                                     │
└──────────────────────────────────────────────────────┘
```

## Responsabilidades de Cada Camada

### ULX - A Linguagem

**O que é:**
- A linguagem que o usuário escreve
- Sintaxe simples e intuitiva
- Abstração de alto nível

**Responsabilidades:**
- Definir a sintaxe
- Ser fácil de aprender
- Ser expressiva e poderosa

**Exemplo:**
```ulx
arquivo = abre("/etc/passwd")
conteudo = le(arquivo)
escreva(conteudo)
fecha(arquivo)
```

### CLX - O Compilador

**O que é:**
- Traduz ULX para C
- Faz análise e otimizações
- Gera código C de alta qualidade

**Responsabilidades:**
- Parse da sintaxe ULX
- Análise semântica
- Geração de código C
- Otimizações de compilação
- Verificação de erros

**Processo:**
```
Código ULX
    ↓
[Lexer - tokenização]
    ↓
[Parser - análise sintática]
    ↓
[Semantic Analyzer - análise semântica]
    ↓
[Optimizer - otimizações]
    ↓
[Code Generator - gera C]
    ↓
Código C otimizado
```

### LX - O Tradutor Hardware

**O que é:**
- Traduz C para assembly nativo
- Acessa syscalls do Linux
- Otimiza para hardware específico

**Responsabilidades:**
- Compilação com GCC/Clang
- Otimizações de hardware (-march=native, -O3, etc)
- Geração de binário estático
- Compatibilidade universal

**Processo:**
```
Código C
    ↓
[GCC/Clang - compilação]
    ↓
[Otimizações de hardware]
    ↓
[Linker - ligação]
    ↓
Binário nativo (assembly)
```

## Fluxo Completo

### 1. Usuário Escreve ULX

```ulx
// programa.ulx
qubit = cria_socket()
conecta(qubit, "0.0.0.0", 8080)
escuta(qubit, 10)

para (i = 0; i < 100; i = i + 1) {
    cliente = aceita(qubit)
    escreva("Cliente conectado")
    fecha(cliente)
}

fecha(qubit)
```

### 2. CLX Compila para C

```bash
$ python3 clx_compiler.py programa.ulx
```

Gera `programa.c`:
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#pragma GCC optimize("O3")
#pragma GCC target("native")

int main() {
    int qubit = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(8080),
        .sin_addr.s_addr = htonl(INADDR_ANY)
    };
    bind(qubit, (struct sockaddr*)&addr, sizeof(addr));
    listen(qubit, 10);
    
    for (int i = 0; i < 100; i++) {
        int cliente = accept(qubit, NULL, NULL);
        printf("Cliente conectado\n");
        close(cliente);
    }
    
    close(qubit);
    return 0;
}
```

### 3. LX Compila para Binário

```bash
$ gcc -O3 -march=native -flto -static programa.c -o programa
```

Gera `programa` (binário nativo)

### 4. Executa no Hardware

```bash
$ ./programa
Cliente conectado
Cliente conectado
...
```

## Vantagens da Arquitetura

### 1. Separação de Responsabilidades
- ULX: foco em linguagem
- CLX: foco em compilação
- LX: foco em hardware

### 2. Modularidade
- Cada camada é independente
- Fácil de estender
- Fácil de otimizar

### 3. Compatibilidade
- ULX funciona em qualquer Linux
- CLX funciona em qualquer máquina
- LX gera binários para qualquer arquitetura

### 4. Performance
- Otimizações em cada nível
- Sem overhead desnecessário
- Tão rápido quanto C puro

## Extensibilidade

### Adicionar Novo Recurso a ULX

1. **Definir sintaxe em ULX**
   ```ulx
   novo_comando(parametros)
   ```

2. **Adicionar parser em CLX**
   ```python
   def parse_novo_comando(self, line):
       # Parse da sintaxe
       return c_code
   ```

3. **Gerar C apropriado**
   ```c
   // Código C equivalente
   ```

4. **LX compila automaticamente**
   ```bash
   gcc -O3 -march=native ...
   ```

### Adicionar Suporte a Nova Arquitetura

1. **LX detecta arquitetura**
   ```bash
   gcc -march=native
   ```

2. **GCC otimiza para a arquitetura**
   ```bash
   gcc -march=arm64 programa.c -o programa.arm64
   ```

3. **Binário funciona na arquitetura**
   ```bash
   ./programa.arm64  # Roda em ARM
   ```

## Comparação com Outras Linguagens

### Python
```
Python Code → Python Interpreter → C Runtime → Hardware
(lento)      (interpretado)       (overhead)
```

### C
```
C Code → GCC → Assembly → Hardware
(difícil)      (rápido)
```

### ULX
```
ULX Code → CLX (otimizado) → C → GCC → Assembly → Hardware
(fácil)    (inteligente)    (rápido)  (nativo)
```

## Conclusão

**ULX é a melhor de ambos os mundos:**

- ✅ **Simplicidade de Python** (ULX)
- ✅ **Performance de C** (CLX + LX)
- ✅ **Compatibilidade universal** (Linux)
- ✅ **Sem dependências** (binário estático)

---

**A arquitetura de três camadas garante:**
1. Facilidade para o usuário (ULX)
2. Otimizações inteligentes (CLX)
3. Performance máxima (LX)
