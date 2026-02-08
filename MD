# 🚀 Guia Completo: Criar uma Linguagem de Programação do Zero para Linux

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura de um Compilador](#arquitetura)
3. [Componentes Principais](#componentes)
4. [Abordagens de Implementação](#abordagens)
5. [Formato ELF - Executáveis Nativos](#formato-elf)
6. [Implementação Passo a Passo](#implementação)
7. [Ferramentas e Bibliotecas](#ferramentas)
8. [Exemplo Prático Completo](#exemplo)

---

## 🎯 Visão Geral {#visão-geral}

Para criar uma linguagem de programação que execute nativamente no Linux, você precisa:

### Objetivos
- ✅ **Parser**: Analisar o código fonte e construir uma AST (Abstract Syntax Tree)
- ✅ **Compilador**: Transformar AST em código de máquina
- ✅ **Gerador ELF**: Produzir binários executáveis no formato ELF
- ✅ **Runtime**: Biblioteca de suporte (opcional)
- ✅ **Syscalls**: Interagir diretamente com o kernel Linux

### Pipeline de Compilação

```
Código Fonte ULX
      ↓
   [LEXER] → Tokens
      ↓
   [PARSER] → AST (Abstract Syntax Tree)
      ↓
   [SEMANTIC ANALYZER] → AST Validada
      ↓
   [CODE GENERATOR]
      ↓
   ┌──────────────────┐
   │  OPÇÃO 1: IR     │
   │  (LLVM IR)       │ → LLVM Backend → ELF
   └──────────────────┘
   ┌──────────────────┐
   │  OPÇÃO 2:        │
   │  Assembly x86-64 │ → Assembler → ELF
   └──────────────────┘
   ┌──────────────────┐
   │  OPÇÃO 3:        │
   │  Bytecode        │ → Transpiler → C → GCC → ELF
   └──────────────────┘
   ┌──────────────────┐
   │  OPÇÃO 4:        │
   │  Binário Direto  │ → Gerador ELF Manual → ELF
   └──────────────────┘
```

---

## 🏗️ Arquitetura de um Compilador {#arquitetura}

### Fase 1: Frontend (Análise)

#### 1.1 Lexer (Análise Léxica)
```
Código:  var x = 10;
         ↓
Tokens:  [VAR] [IDENTIFIER:x] [EQUALS] [NUMBER:10] [SEMICOLON]
```

#### 1.2 Parser (Análise Sintática)
```
Tokens → AST (Árvore Sintática Abstrata)

Exemplo de AST:
    Program
      └── VarDeclaration
            ├── name: "x"
            └── value: IntLiteral(10)
```

#### 1.3 Semantic Analyzer (Análise Semântica)
- Verificação de tipos
- Resolução de símbolos
- Validação de regras da linguagem

### Fase 2: Middle-end (Otimização)

- Otimização de código
- Transformações de AST
- Análise de fluxo de dados

### Fase 3: Backend (Geração de Código)

#### Opções:
1. **Código Assembly x86-64**
2. **LLVM IR** (Intermediate Representation)
3. **Bytecode customizado**
4. **Código de máquina direto**

---

## 🔧 Componentes Principais {#componentes}

### 1. Lexer (Tokenizador)

**Responsabilidade**: Converter texto em tokens

```c
// Exemplo de tokens
typedef enum {
    TOKEN_VAR,
    TOKEN_FUNC,
    TOKEN_IF,
    TOKEN_WHILE,
    TOKEN_RETURN,
    TOKEN_IDENTIFIER,
    TOKEN_NUMBER,
    TOKEN_STRING,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_STAR,
    TOKEN_SLASH,
    TOKEN_EQUALS,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_SEMICOLON,
    TOKEN_EOF
} TokenType;

typedef struct {
    TokenType type;
    char* lexeme;
    int line;
    int column;
} Token;
```

**Implementação básica**:
```c
Token next_token() {
    skip_whitespace();
    
    if (isalpha(current_char)) {
        return read_identifier();
    }
    if (isdigit(current_char)) {
        return read_number();
    }
    if (current_char == '"') {
        return read_string();
    }
    // ... outros casos
}
```

### 2. Parser (Analisador Sintático)

**Responsabilidade**: Construir AST a partir dos tokens

```c
// Estrutura de nós da AST
typedef enum {
    NODE_PROGRAM,
    NODE_FUNC_DECL,
    NODE_VAR_DECL,
    NODE_IF_STMT,
    NODE_WHILE_STMT,
    NODE_RETURN_STMT,
    NODE_BINARY_OP,
    NODE_INT_LITERAL,
    NODE_IDENTIFIER
} NodeType;

typedef struct ASTNode {
    NodeType type;
    union {
        struct {
            char* name;
            struct ASTNode* params;
            struct ASTNode* body;
        } func_decl;
        
        struct {
            char* name;
            struct ASTNode* value;
        } var_decl;
        
        struct {
            char op;
            struct ASTNode* left;
            struct ASTNode* right;
        } binary_op;
        
        int int_value;
        char* string_value;
    } data;
} ASTNode;
```

**Parser recursivo descendente**:
```c
ASTNode* parse_statement() {
    Token tok = peek_token();
    
    switch (tok.type) {
        case TOKEN_VAR:
            return parse_var_declaration();
        case TOKEN_IF:
            return parse_if_statement();
        case TOKEN_WHILE:
            return parse_while_statement();
        case TOKEN_RETURN:
            return parse_return_statement();
        default:
            return parse_expression();
    }
}
```

### 3. Analisador Semântico

**Responsabilidade**: Verificar tipos e regras semânticas

```c
typedef struct {
    char* name;
    Type type;
    int offset; // Para variáveis locais
} Symbol;

typedef struct SymbolTable {
    Symbol* symbols;
    int count;
    struct SymbolTable* parent; // Para escopo aninhado
} SymbolTable;

void semantic_analysis(ASTNode* node, SymbolTable* table) {
    switch (node->type) {
        case NODE_VAR_DECL:
            check_var_declaration(node, table);
            break;
        case NODE_BINARY_OP:
            check_binary_operation(node, table);
            break;
        // ... outros casos
    }
}
```

### 4. Gerador de Código

Aqui temos **4 abordagens principais**:

---

## 🎨 Abordagens de Implementação {#abordagens}

### Abordagem 1: LLVM Backend (Recomendada)

**Vantagens:**
- ✅ Otimizações automáticas de alta qualidade
- ✅ Suporte a múltiplas arquiteturas (x86-64, ARM, etc)
- ✅ Geração de ELF nativa
- ✅ Infraestrutura madura e testada
- ✅ Usado por Rust, Swift, Clang

**Implementação:**

```c
#include <llvm-c/Core.h>
#include <llvm-c/ExecutionEngine.h>
#include <llvm-c/Target.h>
#include <llvm-c/Analysis.h>

// Compilar AST para LLVM IR
LLVMModuleRef compile_to_llvm(ASTNode* ast) {
    // Criar módulo LLVM
    LLVMModuleRef module = LLVMModuleCreateWithName("ulx_module");
    LLVMBuilderRef builder = LLVMCreateBuilder();
    
    // Criar função main
    LLVMTypeRef main_type = LLVMFunctionType(
        LLVMInt32Type(), // retorno int
        NULL, 0,         // sem parâmetros
        0                // não vararg
    );
    
    LLVMValueRef main_func = LLVMAddFunction(
        module, 
        "main", 
        main_type
    );
    
    // Criar bloco básico
    LLVMBasicBlockRef entry = LLVMAppendBasicBlock(main_func, "entry");
    LLVMPositionBuilderAtEnd(builder, entry);
    
    // Gerar código a partir da AST
    generate_llvm_ir(ast, builder, module);
    
    // Retornar 0
    LLVMBuildRet(builder, LLVMConstInt(LLVMInt32Type(), 0, 0));
    
    return module;
}

// Gerar binário ELF
void generate_elf_binary(LLVMModuleRef module, const char* output_file) {
    // Inicializar targets
    LLVMInitializeX86TargetInfo();
    LLVMInitializeX86Target();
    LLVMInitializeX86TargetMC();
    LLVMInitializeX86AsmPrinter();
    
    // Configurar target triple
    char* triple = LLVMGetDefaultTargetTriple();
    LLVMSetTarget(module, triple);
    
    // Criar arquivo objeto
    LLVMTargetRef target;
    char* error = NULL;
    
    if (LLVMGetTargetFromTriple(triple, &target, &error)) {
        fprintf(stderr, "Erro: %s\n", error);
        return;
    }
    
    LLVMTargetMachineRef machine = LLVMCreateTargetMachine(
        target,
        triple,
        "generic",
        "",
        LLVMCodeGenLevelDefault,
        LLVMRelocDefault,
        LLVMCodeModelDefault
    );
    
    // Emitir arquivo objeto
    LLVMTargetMachineEmitToFile(
        machine,
        module,
        output_file,
        LLVMObjectFile,
        &error
    );
}
```

### Abordagem 2: Assembly x86-64 Direto

**Vantagens:**
- ✅ Controle total sobre o código gerado
- ✅ Sem dependências externas
- ✅ Aprendizado profundo de arquitetura

**Desvantagens:**
- ❌ Mais trabalhoso
- ❌ Específico para uma arquitetura

**Implementação:**

```c
void generate_assembly(ASTNode* ast, FILE* output) {
    // Cabeçalho
    fprintf(output, "section .text\n");
    fprintf(output, "global _start\n\n");
    fprintf(output, "_start:\n");
    
    // Gerar código assembly
    generate_asm_node(ast, output);
    
    // Syscall exit
    fprintf(output, "    mov rax, 60\n");   // syscall exit
    fprintf(output, "    xor rdi, rdi\n");  // status 0
    fprintf(output, "    syscall\n");
}

void generate_asm_node(ASTNode* node, FILE* output) {
    switch (node->type) {
        case NODE_INT_LITERAL:
            fprintf(output, "    mov rax, %d\n", node->data.int_value);
            break;
            
        case NODE_BINARY_OP:
            // Gerar código para operando esquerdo
            generate_asm_node(node->data.binary_op.left, output);
            fprintf(output, "    push rax\n");
            
            // Gerar código para operando direito
            generate_asm_node(node->data.binary_op.right, output);
            fprintf(output, "    pop rbx\n");
            
            // Realizar operação
            switch (node->data.binary_op.op) {
                case '+':
                    fprintf(output, "    add rax, rbx\n");
                    break;
                case '-':
                    fprintf(output, "    sub rax, rbx\n");
                    break;
                case '*':
                    fprintf(output, "    imul rax, rbx\n");
                    break;
            }
            break;
    }
}

// Montar com NASM e linkar
void assemble_and_link(const char* asm_file, const char* output) {
    char cmd[512];
    
    // Montar
    sprintf(cmd, "nasm -f elf64 %s -o temp.o", asm_file);
    system(cmd);
    
    // Linkar
    sprintf(cmd, "ld -o %s temp.o", output);
    system(cmd);
}
```

### Abordagem 3: Transpiler para C

**Vantagens:**
- ✅ Extremamente simples de implementar
- ✅ Aproveita otimizações do GCC
- ✅ Funciona em qualquer plataforma

**Desvantagens:**
- ❌ Dependência do GCC
- ❌ Menos controle

**Implementação:**

```c
void transpile_to_c(ASTNode* ast, FILE* output) {
    // Includes
    fprintf(output, "#include <stdio.h>\n");
    fprintf(output, "#include <stdlib.h>\n");
    fprintf(output, "#include <unistd.h>\n");
    fprintf(output, "#include <sys/syscall.h>\n\n");
    
    // Runtime functions
    fprintf(output, "void ulx_print(int n) {\n");
    fprintf(output, "    printf(\"%%d\\n\", n);\n");
    fprintf(output, "}\n\n");
    
    // Main
    fprintf(output, "int main() {\n");
    
    transpile_node(ast, output, 1);
    
    fprintf(output, "    return 0;\n");
    fprintf(output, "}\n");
}

void transpile_node(ASTNode* node, FILE* output, int indent) {
    switch (node->type) {
        case NODE_VAR_DECL:
            fprintf(output, "%*sint %s = ", indent * 4, "", 
                    node->data.var_decl.name);
            transpile_node(node->data.var_decl.value, output, 0);
            fprintf(output, ";\n");
            break;
            
        case NODE_INT_LITERAL:
            fprintf(output, "%d", node->data.int_value);
            break;
    }
}

// Compilar com GCC
void compile_c_to_elf(const char* c_file, const char* output) {
    char cmd[512];
    sprintf(cmd, "gcc -o %s %s -static -O2", output, c_file);
    system(cmd);
}
```

### Abordagem 4: Gerador ELF Manual (Avançado)

**Vantagens:**
- ✅ Máximo controle
- ✅ Binários mínimos
- ✅ Zero dependências

**Desvantagens:**
- ❌ Muito complexo
- ❌ Requer conhecimento profundo de ELF

**Implementação básica:**

```c
#include <elf.h>
#include <string.h>

typedef struct {
    uint8_t* code;
    size_t code_size;
    uint8_t* data;
    size_t data_size;
} Program;

void write_elf_binary(Program* prog, const char* filename) {
    FILE* f = fopen(filename, "wb");
    
    // ELF Header
    Elf64_Ehdr ehdr = {0};
    memcpy(ehdr.e_ident, ELFMAG, SELFMAG);
    ehdr.e_ident[EI_CLASS] = ELFCLASS64;
    ehdr.e_ident[EI_DATA] = ELFDATA2LSB;
    ehdr.e_ident[EI_VERSION] = EV_CURRENT;
    ehdr.e_ident[EI_OSABI] = ELFOSABI_LINUX;
    
    ehdr.e_type = ET_EXEC;
    ehdr.e_machine = EM_X86_64;
    ehdr.e_version = EV_CURRENT;
    ehdr.e_entry = 0x401000; // Endereço de entrada
    ehdr.e_phoff = sizeof(Elf64_Ehdr);
    ehdr.e_ehsize = sizeof(Elf64_Ehdr);
    ehdr.e_phentsize = sizeof(Elf64_Phdr);
    ehdr.e_phnum = 1; // Um program header
    
    fwrite(&ehdr, sizeof(ehdr), 1, f);
    
    // Program Header
    Elf64_Phdr phdr = {0};
    phdr.p_type = PT_LOAD;
    phdr.p_flags = PF_X | PF_R; // Executável e legível
    phdr.p_offset = 0x1000;
    phdr.p_vaddr = 0x401000;
    phdr.p_paddr = 0x401000;
    phdr.p_filesz = prog->code_size;
    phdr.p_memsz = prog->code_size;
    phdr.p_align = 0x1000;
    
    fwrite(&phdr, sizeof(phdr), 1, f);
    
    // Padding até 0x1000
    fseek(f, 0x1000, SEEK_SET);
    
    // Escrever código
    fwrite(prog->code, prog->code_size, 1, f);
    
    fclose(f);
    chmod(filename, 0755); // Tornar executável
}

// Exemplo: gerar código de máquina para "mov rax, 42; syscall exit"
void generate_hello_world() {
    Program prog;
    
    // Código de máquina x86-64
    uint8_t code[] = {
        // mov rax, 1 (syscall write)
        0x48, 0xc7, 0xc0, 0x01, 0x00, 0x00, 0x00,
        // mov rdi, 1 (stdout)
        0x48, 0xc7, 0xc7, 0x01, 0x00, 0x00, 0x00,
        // lea rsi, [rel msg]
        0x48, 0x8d, 0x35, 0x0d, 0x00, 0x00, 0x00,
        // mov rdx, 13 (tamanho)
        0x48, 0xc7, 0xc2, 0x0d, 0x00, 0x00, 0x00,
        // syscall
        0x0f, 0x05,
        // mov rax, 60 (syscall exit)
        0x48, 0xc7, 0xc0, 0x3c, 0x00, 0x00, 0x00,
        // xor rdi, rdi
        0x48, 0x31, 0xff,
        // syscall
        0x0f, 0x05,
        // msg: "Hello, World!"
        'H', 'e', 'l', 'l', 'o', ',', ' ', 
        'W', 'o', 'r', 'l', 'd', '!', '\n'
    };
    
    prog.code = code;
    prog.code_size = sizeof(code);
    
    write_elf_binary(&prog, "hello");
}
```

---

## 📦 Formato ELF - Executáveis Nativos {#formato-elf}

### Estrutura do ELF

```
┌─────────────────────┐
│   ELF Header        │  ← Informações básicas
├─────────────────────┤
│   Program Headers   │  ← Como carregar na memória
├─────────────────────┤
│   .text (código)    │  ← Instruções de máquina
├─────────────────────┤
│   .data (dados)     │  ← Variáveis inicializadas
├─────────────────────┤
│   .bss (BSS)        │  ← Variáveis não inicializadas
├─────────────────────┤
│   .rodata           │  ← Constantes (read-only)
├─────────────────────┤
│   Section Headers   │  ← Metadados das seções
└─────────────────────┘
```

### ELF Header

```c
typedef struct {
    unsigned char e_ident[16];  // Magic number + info
    uint16_t e_type;            // Tipo (executável, shared, etc)
    uint16_t e_machine;         // Arquitetura (x86-64, ARM, etc)
    uint32_t e_version;         // Versão
    uint64_t e_entry;           // Ponto de entrada
    uint64_t e_phoff;           // Offset dos program headers
    uint64_t e_shoff;           // Offset dos section headers
    uint32_t e_flags;           // Flags
    uint16_t e_ehsize;          // Tamanho do ELF header
    uint16_t e_phentsize;       // Tamanho de cada program header
    uint16_t e_phnum;           // Número de program headers
    uint16_t e_shentsize;       // Tamanho de cada section header
    uint16_t e_shnum;           // Número de section headers
    uint16_t e_shstrndx;        // Index da seção de strings
} Elf64_Ehdr;
```

### Program Header

```c
typedef struct {
    uint32_t p_type;    // Tipo do segmento (LOAD, DYNAMIC, etc)
    uint32_t p_flags;   // Permissões (R/W/X)
    uint64_t p_offset;  // Offset no arquivo
    uint64_t p_vaddr;   // Endereço virtual
    uint64_t p_paddr;   // Endereço físico
    uint64_t p_filesz;  // Tamanho no arquivo
    uint64_t p_memsz;   // Tamanho na memória
    uint64_t p_align;   // Alinhamento
} Elf64_Phdr;
```

### Como o Linux Carrega um ELF

1. **Kernel lê o ELF header**
2. **Valida o magic number** (0x7F E L F)
3. **Lê os program headers**
4. **Para cada PT_LOAD**:
   - Mapeia o segmento na memória (mmap)
   - Define permissões (RWX)
5. **Salta para e_entry** (ponto de entrada)

---

## 🛠️ Implementação Passo a Passo {#implementação}

### Passo 1: Definir a Sintaxe da Linguagem

```
// Exemplo de sintaxe ULX
func main() -> i32 {
    var x: i32 = 10;
    var y: i32 = 20;
    
    if (x < y) {
        print("x é menor");
    }
    
    return 0;
}
```

### Passo 2: Implementar o Lexer

```c
typedef struct {
    const char* start;
    const char* current;
    int line;
} Lexer;

Token scan_token(Lexer* lexer) {
    skip_whitespace(lexer);
    
    if (is_at_end(lexer)) return make_token(TOKEN_EOF);
    
    char c = advance(lexer);
    
    if (isalpha(c)) return identifier(lexer);
    if (isdigit(c)) return number(lexer);
    
    switch (c) {
        case '(': return make_token(TOKEN_LPAREN);
        case ')': return make_token(TOKEN_RPAREN);
        case '{': return make_token(TOKEN_LBRACE);
        case '}': return make_token(TOKEN_RBRACE);
        case ';': return make_token(TOKEN_SEMICOLON);
        case '+': return make_token(TOKEN_PLUS);
        case '-': return make_token(TOKEN_MINUS);
        case '*': return make_token(TOKEN_STAR);
        case '/': return make_token(TOKEN_SLASH);
    }
    
    return error_token("Unexpected character");
}
```

### Passo 3: Implementar o Parser

```c
ASTNode* parse_program() {
    ASTNode* program = create_node(NODE_PROGRAM);
    
    while (!match(TOKEN_EOF)) {
        ASTNode* stmt = parse_statement();
        add_child(program, stmt);
    }
    
    return program;
}

ASTNode* parse_statement() {
    if (match(TOKEN_VAR)) return parse_var_decl();
    if (match(TOKEN_FUNC)) return parse_func_decl();
    if (match(TOKEN_IF)) return parse_if_stmt();
    if (match(TOKEN_WHILE)) return parse_while_stmt();
    if (match(TOKEN_RETURN)) return parse_return_stmt();
    
    return parse_expression_stmt();
}
```

### Passo 4: Análise Semântica

```c
void analyze_semantics(ASTNode* ast) {
    SymbolTable* global = create_symbol_table(NULL);
    
    check_node(ast, global);
    
    if (has_errors()) {
        print_errors();
        exit(1);
    }
}
```

### Passo 5: Geração de Código (Escolher abordagem)

**Opção LLVM:**
```c
int main(int argc, char** argv) {
    // 1. Ler código fonte
    char* source = read_file(argv[1]);
    
    // 2. Lexer
    Lexer lexer = init_lexer(source);
    Token* tokens = tokenize(&lexer);
    
    // 3. Parser
    Parser parser = init_parser(tokens);
    ASTNode* ast = parse(&parser);
    
    // 4. Semantic analysis
    analyze_semantics(ast);
    
    // 5. Gerar LLVM IR
    LLVMModuleRef module = compile_to_llvm(ast);
    
    // 6. Gerar ELF
    generate_elf_binary(module, "output");
    
    printf("Compilação concluída: output\n");
    return 0;
}
```

---

## 🔨 Ferramentas e Bibliotecas {#ferramentas}

### Para Parser

1. **Flex + Bison** (C)
   - Geradores de lexer e parser
   - Muito usados em produção

2. **ANTLR** (Java/C++/Python)
   - Gerador de parser LL(*)
   - Suporta múltiplas linguagens

3. **Parser manual recursivo descendente**
   - Mais controle
   - Melhor para aprendizado

### Para Backend

1. **LLVM** (Recomendado)
   ```bash
   sudo apt install llvm-dev clang
   ```

2. **NASM** (Assembly)
   ```bash
   sudo apt install nasm
   ```

3. **libelf** (Manipulação ELF)
   ```bash
   sudo apt install libelf-dev
   ```

### Ferramentas de Análise

```bash
# Ver estrutura ELF
readelf -h programa
readelf -l programa
readelf -S programa

# Desmontar código
objdump -d programa

# Ver dependências
ldd programa

# Ver símbolos
nm programa
```

---

## 📚 Exemplo Prático Completo {#exemplo}

Vou criar um compilador minimalista completo que compila uma linguagem simples para ELF:

### Linguagem: SimpleCalc

```
// Exemplo de código SimpleCalc
10 + 20 * 3
```

### Compilador Completo

```c
// calc_compiler.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <sys/stat.h>
#include <elf.h>

// ============ LEXER ============
typedef enum {
    TOKEN_NUMBER,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_STAR,
    TOKEN_SLASH,
    TOKEN_EOF
} TokenType;

typedef struct {
    TokenType type;
    int value;
} Token;

Token* tokenize(const char* source, int* count) {
    Token* tokens = malloc(sizeof(Token) * 100);
    int i = 0;
    const char* p = source;
    
    while (*p) {
        if (isspace(*p)) {
            p++;
            continue;
        }
        
        if (isdigit(*p)) {
            tokens[i].type = TOKEN_NUMBER;
            tokens[i].value = atoi(p);
            while (isdigit(*p)) p++;
            i++;
            continue;
        }
        
        switch (*p) {
            case '+': tokens[i++].type = TOKEN_PLUS; break;
            case '-': tokens[i++].type = TOKEN_MINUS; break;
            case '*': tokens[i++].type = TOKEN_STAR; break;
            case '/': tokens[i++].type = TOKEN_SLASH; break;
        }
        p++;
    }
    
    tokens[i].type = TOKEN_EOF;
    *count = i;
    return tokens;
}

// ============ GERADOR DE CÓDIGO ============
void generate_x86_code(Token* tokens, int count, uint8_t** code, size_t* size) {
    uint8_t buffer[1024];
    int pos = 0;
    
    // mov rax, primeiro_numero
    buffer[pos++] = 0x48; buffer[pos++] = 0xc7; buffer[pos++] = 0xc0;
    *(int32_t*)&buffer[pos] = tokens[0].value; pos += 4;
    
    for (int i = 1; i < count; i += 2) {
        if (i + 1 >= count) break;
        
        // mov rbx, proximo_numero
        buffer[pos++] = 0x48; buffer[pos++] = 0xc7; buffer[pos++] = 0xc3;
        *(int32_t*)&buffer[pos] = tokens[i+1].value; pos += 4;
        
        // Operação
        switch (tokens[i].type) {
            case TOKEN_PLUS:
                buffer[pos++] = 0x48; buffer[pos++] = 0x01;
                buffer[pos++] = 0xd8; // add rax, rbx
                break;
            case TOKEN_MINUS:
                buffer[pos++] = 0x48; buffer[pos++] = 0x29;
                buffer[pos++] = 0xd8; // sub rax, rbx
                break;
            case TOKEN_STAR:
                buffer[pos++] = 0x48; buffer[pos++] = 0x0f;
                buffer[pos++] = 0xaf; buffer[pos++] = 0xc3; // imul rax, rbx
                break;
        }
    }
    
    // Syscall exit com resultado em rdi
    buffer[pos++] = 0x48; buffer[pos++] = 0x89;
    buffer[pos++] = 0xc7; // mov rdi, rax
    buffer[pos++] = 0x48; buffer[pos++] = 0xc7;
    buffer[pos++] = 0xc0; buffer[pos++] = 0x3c;
    buffer[pos++] = 0x00; buffer[pos++] = 0x00;
    buffer[pos++] = 0x00; // mov rax, 60
    buffer[pos++] = 0x0f; buffer[pos++] = 0x05; // syscall
    
    *code = malloc(pos);
    memcpy(*code, buffer, pos);
    *size = pos;
}

// ============ GERADOR ELF ============
void write_elf(const char* filename, uint8_t* code, size_t code_size) {
    FILE* f = fopen(filename, "wb");
    
    Elf64_Ehdr ehdr = {0};
    memcpy(ehdr.e_ident, ELFMAG, SELFMAG);
    ehdr.e_ident[EI_CLASS] = ELFCLASS64;
    ehdr.e_ident[EI_DATA] = ELFDATA2LSB;
    ehdr.e_ident[EI_VERSION] = EV_CURRENT;
    ehdr.e_ident[EI_OSABI] = ELFOSABI_LINUX;
    
    ehdr.e_type = ET_EXEC;
    ehdr.e_machine = EM_X86_64;
    ehdr.e_version = EV_CURRENT;
    ehdr.e_entry = 0x401000;
    ehdr.e_phoff = sizeof(Elf64_Ehdr);
    ehdr.e_ehsize = sizeof(Elf64_Ehdr);
    ehdr.e_phentsize = sizeof(Elf64_Phdr);
    ehdr.e_phnum = 1;
    
    fwrite(&ehdr, sizeof(ehdr), 1, f);
    
    Elf64_Phdr phdr = {0};
    phdr.p_type = PT_LOAD;
    phdr.p_flags = PF_X | PF_R;
    phdr.p_offset = 0x1000;
    phdr.p_vaddr = 0x401000;
    phdr.p_paddr = 0x401000;
    phdr.p_filesz = code_size;
    phdr.p_memsz = code_size;
    phdr.p_align = 0x1000;
    
    fwrite(&phdr, sizeof(phdr), 1, f);
    
    fseek(f, 0x1000, SEEK_SET);
    fwrite(code, code_size, 1, f);
    
    fclose(f);
    chmod(filename, 0755);
}

// ============ MAIN ============
int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "Uso: %s <expressao>\n", argv[0]);
        return 1;
    }
    
    // Tokenizar
    int token_count;
    Token* tokens = tokenize(argv[1], &token_count);
    
    // Gerar código x86-64
    uint8_t* code;
    size_t code_size;
    generate_x86_code(tokens, token_count, &code, &code_size);
    
    // Escrever ELF
    write_elf("calc", code, code_size);
    
    printf("✓ Compilado com sucesso: ./calc\n");
    
    free(tokens);
    free(code);
    
    return 0;
}
```

### Compilar e Testar

```bash
# Compilar o compilador
gcc -o calc_compiler calc_compiler.c

# Usar o compilador
./calc_compiler "10 + 20"

# Executar o programa gerado
./calc
echo $?  # Deve mostrar 30
```

---

## 🎓 Recursos de Aprendizado

### Livros
1. **"Crafting Interpreters"** - Robert Nystrom
2. **"Engineering a Compiler"** - Keith Cooper
3. **"The Dragon Book"** - Aho, Sethi, Ullman

### Documentação
- [LLVM Tutorial](https://llvm.org/docs/tutorial/)
- [ELF Specification](https://refspecs.linuxfoundation.org/elf/elf.pdf)
- [x86-64 ABI](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf)

### Ferramentas Online
- [Compiler Explorer](https://godbolt.org/)
- [LLVM IR Explorer](https://llvm.org/docs/LangRef.html)

---

## 🚦 Roadmap Recomendado

### Fase 1: Básico (1-2 semanas)
- ✅ Lexer simples
- ✅ Parser para expressões
- ✅ Gerador de assembly básico

### Fase 2: Intermediário (1-2 meses)
- ✅ Statements (if, while, functions)
- ✅ Sistema de tipos
- ✅ Análise semântica

### Fase 3: Avançado (3-6 meses)
- ✅ Backend LLVM completo
- ✅ Otimizações
- ✅ Biblioteca padrão
- ✅ Gerenciamento de memória

### Fase 4: Produção (6+ meses)
- ✅ Depuração
- ✅ Mensagens de erro
- ✅ Tooling (LSP, formatter)
- ✅ Documentação

---

## 🎯 Conclusão

Criar uma linguagem de programação é um projeto ambicioso mas realizável! As chaves para o sucesso são:

1. **Comece simples** - Implemente features gradualmente
2. **Use ferramentas** - LLVM, ANTLR, etc economizam muito tempo
3. **Estude exemplos** - Analise outras linguagens
4. **Teste constantemente** - Escreva testes para cada feature
5. **Documente** - Tanto o código quanto a linguagem

**Recomendação para ULX**: Use LLVM para o backend e foque em criar uma linguagem expressiva e segura!

---

**Autor**: Claude AI  
**Data**: Fevereiro 2026  
**Licença**: MIT
