#!/bin/bash

# ULX UNIVERSAL BRIDGE - CAMADA DE EXECUÇÃO NATIVA (.EXE & .APK)
# Este script registra os formatos .exe e .apk no kernel via binfmt_misc de forma persistente.

# NÃO USAR set -e: Tratamento de erros personalizado para feedback ao usuário

# Cores para mensagens no terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

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
trap 'LAST_COMMAND=$BASH_COMMAND; error_handler' ERR

# Funções de log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

log_info "========================================================="
log_info "   ULX - PONTE UNIVERSAL DE EXECUÇÃO (.EXE & .APK)"
log_info "========================================================="

# 1. Verificar e montar binfmt_misc se necessário
if [ ! -d /proc/sys/fs/binfmt_misc ]; then
    log_info "[KERNEL] Montando binfmt_misc..."
    sudo mount -t binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc || error_handler
fi

# 2. Remover associações conflitantes do Wine (se existirem)
# O Wine costuma registrar 'wine' ou 'DOSWin' no binfmt_misc.
# Vamos desativar temporariamente para que o ULX tenha prioridade.
for conflict in wine DOSWin; do
    if [ -f "/proc/sys/fs/binfmt_misc/$conflict" ]; then
        log_info "[KERNEL] Removendo conflito de binfmt: $conflict"
        echo -1 | sudo tee "/proc/sys/fs/binfmt_misc/$conflict" > /dev/null || true
    fi
done

# 3. Criar Wrappers de Execução Silenciosa
log_info "Criando wrappers de execução para .EXE e .APK..."

# Wrapper para .EXE
cat <<EOF | sudo tee /usr/local/bin/ulx-run-exe > /dev/null
#!/bin/bash
# ULX-EXE Wrapper: Execução silenciosa sem emulador visível.
# Usa Wine apenas como tradutor de syscalls, com otimizações ULX.
export WINEDEBUG=-all
export LD_PRELOAD="/usr/local/lib/ulx/runtime/libulx_core.so"
export VK_LAYER_PATH="/usr/local/lib/ulx/runtime/"
export VK_INSTANCE_LAYERS="VK_LAYER_ULX_OPTIMIZER"
export ULX_GPU_ENABLED=1
# Executa o Wine de forma silenciosa e passa todos os argumentos
exec wine "\$@" || exit 1
EOF
sudo chmod +x /usr/local/bin/ulx-run-exe || error_handler

# Wrapper para .APK
cat <<EOF | sudo tee /usr/local/bin/ulx-run-apk > /dev/null
#!/bin/bash
# ULX-APK Wrapper: Execução nativa de apps Android via Anbox.
export LD_PRELOAD="/usr/local/lib/ulx/runtime/libulx_core.so"
export VK_LAYER_PATH="/usr/local/lib/ulx/runtime/"
export VK_INSTANCE_LAYERS="VK_LAYER_ULX_OPTIMIZER"

# Verifica se o anbox-session-manager está rodando
ping -c 1 127.0.0.1 > /dev/null || sudo systemctl start anbox-container-manager.service

exec anbox-shell --app="\$1" || exec anbox-shell --file="\$1" || exit 1
EOF
sudo chmod +x /usr/local/bin/ulx-run-apk || error_handler

# 4. Criar arquivos de configuração binfmt para persistência
log_info "Criando configurações binfmt_misc persistentes em /etc/binfmt.d/ ..."

# Configuração para .EXE (Usando prioridade alta e nome único)
# O prefixo :ulx-exe: garante que nossa regra seja carregada.
cat <<EOF | sudo tee /etc/binfmt.d/ulx-exe.conf > /dev/null
:ulx-exe:M::MZ::/usr/local/bin/ulx-run-exe:P
EOF

# Configuração para .APK
cat <<EOF | sudo tee /etc/binfmt.d/ulx-apk.conf > /dev/null
:ulx-apk:M::PK\x03\x04::/usr/local/bin/ulx-run-apk:P
EOF

# 5. Recarregar configurações do binfmt_misc
log_info "Recarregando configurações do systemd-binfmt..."
sudo systemctl restart systemd-binfmt || error_handler

log_info "========================================================="
log_info "PONTE UNIVERSAL ATIVADA COM PRIORIDADE MÁXIMA!"
log_info "O ULX agora interceptará arquivos .exe antes do Wine padrão."
log_info "========================================================="
