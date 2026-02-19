# Arquitetura ULX-Core: Especificação Técnica de Alto Nível

Este documento detalha a arquitetura do **ULX Interceptor**, um sistema de interceptação e tradução de baixo nível projetado para extrair o máximo desempenho do hardware **Intel Sandy Bridge** (i7-2760QM) e sua GPU integrada no **Arch Linux**.

## 1. Visão Geral do Sistema
O ULX atua como uma camada de abstração e otimização entre as aplicações e o hardware, operando em dois domínios principais:
- **ULX-CPU (Core)**: Interceptação de instruções e gerenciamento de recursos de baixo nível.
- **ULX-GPU (Vulkan Layer)**: Interceptação e otimização de fluxos de comandos gráficos.

## 2. Componentes de CPU (ULX-Core)

### 2.1 Motor de Interceptação JIT (Just-In-Time)
Para o processador i7-2760QM, o ULX implementa um motor de tradução binária dinâmica que foca em:
- **Vetorização AVX**: Tradução automática de loops escalares e instruções SSE antigas para o conjunto de instruções **AVX (Advanced Vector Extensions)** nativo da Sandy Bridge, permitindo processar mais dados por ciclo de clock.
- **Otimização de Micro-op (uOp)**: Reordenação de instruções para maximizar o uso das unidades de execução e evitar *stalls* no pipeline.

### 2.2 Alocador de Memória "Slab-Symmetry"
Um alocador de memória customizado que substitui o `malloc` padrão por um sistema de **Slab Allocation** alinhado a 64 bytes:
- **Alinhamento de Cache Line**: Garante que todas as estruturas de dados críticas comecem no início de uma linha de cache L1 (64 bytes), eliminando o fenômeno de *false sharing* e reduzindo a latência de acesso.
- **Zero-Copy Buffers**: Implementação de buffers compartilhados entre CPU e GPU para evitar cópias de memória desnecessárias durante a transferência de texturas e vértices.

## 3. Componentes de GPU (ULX-Vulkan)

### 3.1 Vulkan Implicit Layer
Diferente de um simples wrapper, o ULX-GPU é implementado como uma **Vulkan Implicit Layer**. Isso permite:
- **Interceptação de Command Buffers**: O ULX analisa os `VkCommandBuffer` antes de serem submetidos às filas da GPU (`vkQueueSubmit`).
- **Poda de Draw Calls (Draw Call Pruning)**: Identificação e remoção de comandos de desenho redundantes ou invisíveis (occlusion culling em nível de driver), aliviando drasticamente a carga na GPU integrada.

### 3.2 Tradutor de Shaders "Nexus"
Uma camada que intercepta o código SPIR-V e aplica otimizações específicas para a arquitetura de execução da Intel (Gen6):
- **Otimização de Registradores**: Reorganiza o uso de registradores nos shaders para permitir maior paralelismo (threads simultâneas) na GPU.
- **Cache de Shaders Persistente**: Armazenamento em disco de shaders já traduzidos e otimizados para evitar *stuttering* durante o jogo.

## 4. Estratégia de Estabilidade e Segurança
- **Fallback Automático**: Se uma tradução falhar ou causar instabilidade, o ULX reverte instantaneamente para o comando original.
- **Monitoramento em Tempo Real**: Um watchdog que observa a temperatura e o uso do hardware, ajustando o nível de otimização para evitar *thermal throttling*.
