# ULX Interceptor & Translation Layer

Este projeto visa criar uma camada de interceptação e tradução de baixo nível para o **Arch Linux**, atuando entre o sistema operacional/aplicações e o hardware (**CPU/GPU**).

## 📂 Estrutura do Projeto

- **/cpu**: Implementações de interceptação de chamadas de sistema (Syscalls) e instruções de processador via `LD_PRELOAD` e `eBPF`.
- **/gpu**: Camada de tradução gráfica para interceptação de Command Buffers via `Vulkan Layers` e wrappers OpenGL.
- **/docs**: Documentação técnica detalhada sobre o funcionamento da camada de tradução.

## 🚀 Objetivos

1. Interceptar dados em tempo real antes de chegarem ao hardware.
2. Aplicar uma camada de tradução customizada para otimização ou compatibilidade.
3. Manter a transparência para as aplicações do usuário.
