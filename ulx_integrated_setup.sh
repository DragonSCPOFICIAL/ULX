#!/bin/bash

# ULX INTEGRATED SETUP - SISTEMA DE PERFORMANCE DE METAL (Arch Linux)
# Este script integra o ULX Interceptor com a Linguagem de Programação ULX.

# NÃO USAR set -e: Tratamento de erros personalizado para feedback ao usuário

# Cores
RED=\'\033[0;31m\'
GREEN=\'\033[0;32m\'
YELLOW=\'\033[1;33m\'
NC=\'\033[0m\'

# Variável para armazenar o último comando executado
LAST_COMMAND=""

# Função de log de erro personalizada
error_handler() {
    local last_exit_code=$?
    local last_command="${LAST_COMMAND}"
    echo -e "${RED}[ERRO]${NC} Um erro ocorreu! Código de saída: ${last_exit_code}"
    echo -e "${RED}[ERRO]${NC} Comando que falhou: ${last_command}"
    echo -e "${RED}[ERRO]${NC} Por favor, revise as mensagens acima para detalhes do erro."
    echo -e "${RED}Pressione ENTER para continuar (pode causar mais erros) ou CTRL+C para abortar.${NC}"
    read -r
    return 1 # Indica falha
}

# Configurar trap para capturar erros
trap \'LAST_COMMAND=$BASH_COMMAND; error_handler\' ERR

# Funções de log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

log_info "========================================================="
log_info "   ULX - SISTEMA DE PERFORMANCE DE METAL (v2.1.0)"
log_info "========================================================="

# 1. Configurar o Compilador ULX para Performance
log_info "[ULX] Configurando pipeline de compilação \'Metal\'..."
# Ativar otimizações de AVX e Syscalls diretas no compilador Python
export ULX_OPTIMIZE_AVX=1
export ULX_USE_DIRECT_SYSCALLS=1

# 2. Compilar o Interceptor de Baixo Nível
log_info "[INTERCEPTOR] Compilando ULX-Core e ULX-Vulkan..."
mkdir -p ulx-interceptor/build && cd ulx-interceptor/build || error_handler
cmake .. -DCMAKE_BUILD_TYPE=Release || error_handler
make -j$(nproc) || error_handler
cd ../.. || error_handler

# 3. Integrar com a Linguagem ULX
log_info "[INTEGRATION] Vinculando a linguagem ULX ao Interceptor..."
# Copiar as bibliotecas compartilhadas para o diretório de runtime da linguagem
sudo mkdir -p /usr/local/lib/ulx/runtime || error_handler
sudo cp ulx-interceptor/build/libulx_core.so /usr/local/lib/ulx/runtime/ || error_handler
sudo cp ulx-interceptor/build/libulx_vulkan.so /usr/local/lib/ulx/runtime/ || error_handler
sudo cp ulx-interceptor/gpu/ulx_vulkan_layer.json /usr/local/lib/ulx/runtime/ || error_handler

# 4. Criar o Wrapper de Execução \'ulx-run\'
log_info "[BIN] Criando utilitário \'ulx-run\' para execução otimizada..."
cat <<EOF | sudo tee /usr/local/bin/ulx-run > /dev/null
#!/bin/bash
# ULX-RUN: Executa binários ULX com interceptação e otimização total.
export LD_PRELOAD="/usr/local/lib/ulx/runtime/libulx_core.so"
export VK_LAYER_PATH="/usr/local/lib/ulx/runtime/"
export VK_INSTANCE_LAYERS="VK_LAYER_ULX_OPTIMIZER"
export ULX_GPU_ENABLED=1
exec "\$@" || exit 1
EOF
sudo chmod +x /usr/local/bin/ulx-run || error_handler

log_info "========================================================="
log_info "INTEGRAÇÃO CONCLUÍDA: O ULX agora é uma linguagem de METAL."
log_info "1. Compile seu código: ulxc seu_programa.ulx -o programa"
log_info "2. Rode com performance total: ulx-run ./programa"
log_info "========================================================="
