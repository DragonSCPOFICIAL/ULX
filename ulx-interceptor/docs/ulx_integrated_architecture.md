# Arquitetura Integrada: ULX + Interceptor (Performance de Metal)

Esta documentação descreve a integração da linguagem **ULX** com o **ULX Interceptor**, transformando o ecossistema em uma plataforma de desenvolvimento de performance extrema para **Arch Linux**.

## 1. O Conceito "Native-to-Metal"
A linguagem ULX foi projetada para eliminar abstrações. Com a integração do Interceptor, ela passa a ter as seguintes capacidades nativas:

- **LNX (Runtime)**: Uso de syscalls diretas do Linux (sem `libc`).
- **ULX-Core (CPU)**: Alocação de memória via **Slab Allocator** alinhado (64 bytes) e vetorização automática **AVX**.
- **ULX-GPU (Vulkan)**: Comandos de GPU integrados na sintaxe que falam diretamente com a **Vulkan Layer**.

## 2. Fluxo de Compilação Otimizado
```
Código Fonte (.ulx) 
       │
       ▼
[Parser] -> AST
       │
       ▼
[Type Checker] -> Typed AST
       │
       ▼
[AST to IR] -> ULX-IR (Com Opcodes AVX/GPU)
       │
       ▼
[CodeGen x86-64] -> Assembly Otimizado (-march=sandybridge)
       │
       ▼
[ELF Generator] -> Binário Standalone Estático
```

## 3. Integração de Hardware
### 3.1 Vetorização AVX
O compilador identifica padrões de loops e operações em arrays e emite instruções `vaddps`, `vmovaps`, etc. Isso permite processar até 8 números de ponto flutuante simultaneamente no i7-2760QM.

### 3.2 Interceptação de GPU
Ao usar a instrução `gpu_submit()` na linguagem ULX, o binário gerado faz uma chamada de sistema otimizada que é interceptada pela **ULX Vulkan Layer**, permitindo que a GPU processe dados sem o overhead de drivers pesados.

## 4. Como Usar a Integração
1. Compile o Interceptor: `./ulx_build_and_run.sh`
2. Compile seu código ULX: `ulxc seu_programa.ulx -o programa`
3. Execute com otimização total: `LD_PRELOAD=./libulx_core.so ./programa`
