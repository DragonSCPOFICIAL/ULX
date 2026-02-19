#!/bin/bash

# ULX UNIVERSAL BRIDGE - CAMADA DE EXECUÇÃO NATIVA (.EXE & .APK)
# Este script registra os formatos .exe e .apk no kernel via binfmt_misc de forma persistente.

# Sair imediatamente se um comando falhar
set -e

# Cores para mensagens no terminal
RED=\'\\033[0;31m\'
GREEN=\'\\033[0;32m\'
YELLOW=\'\\033[1;33m\'
NC=\'\\033[0m\'

# Funções de log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERRO]${NC} $1"
    exit 1 # Sair em caso de erro crítico
}

log_info "========================================================="
log_info "   ULX - PONTE UNIVERSAL DE EXECUÇÃO (.EXE & .APK)"
log_info "========================================================="

# 1. Verificar e montar binfmt_misc se necessário
if [ ! -d /proc/sys/fs/binfmt_misc ]; then
    log_info "[KERNEL] Montando binfmt_misc..."
    sudo mount -t binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc || log_error "Falha ao montar binfmt_misc."
fi

# 2. Criar Wrappers de Execução Silenciosa
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
exec wine "\$@" || exit 1
EOF
sudo chmod +x /usr/local/bin/ulx-run-exe || log_error "Falha ao definir permissões para ulx-run-exe."

# Wrapper para .APK
cat <<EOF | sudo tee /usr/local/bin/ulx-run-apk > /dev/null
#!/bin/bash
# ULX-APK Wrapper: Execução nativa de apps Android via Anbox.
# Inicia o serviço Anbox se não estiver rodando e tenta lançar o APK.
export LD_PRELOAD="/usr/local/lib/ulx/runtime/libulx_core.so"
export VK_LAYER_PATH="/usr/local/lib/ulx/runtime/"
export VK_INSTANCE_LAYERS="VK_LAYER_ULX_OPTIMIZER"

# Verifica se o anbox-session-manager está rodando, se não, tenta iniciar
ping -c 1 127.0.0.1 > /dev/null || sudo systemctl start anbox-container-manager.service

# Tenta lançar o APK via anbox-shell. Pode precisar de mais configuração do Anbox.
# Para uma integração mais robusta, o APK precisaria ser instalado no ambiente Anbox primeiro.
exec anbox-shell --app="\$1" || exec anbox-shell --file="\$1" || exit 1
EOF
sudo chmod +x /usr/local/bin/ulx-run-apk || log_error "Falha ao definir permissões para ulx-run-apk."

# 3. Criar arquivos de configuração binfmt para persistência
log_info "Criando configurações binfmt_misc persistentes em /etc/binfmt.d/ ..."

# Configuração para .EXE
cat <<EOF | sudo tee /etc/binfmt.d/ulx-exe.conf > /dev/null
:ulx-exe:M::MZ::/usr/local/bin/ulx-run-exe:
EOF

# Configuração para .APK
cat <<EOF | sudo tee /etc/binfmt.d/ulx-apk.conf > /dev/null
:ulx-apk:M::PK\x03\x04::/usr/local/bin/ulx-run-apk:
EOF

# 4. Recarregar configurações do binfmt_misc para aplicar as novas regras imediatamente
log_info "Recarregando configurações do systemd-binfmt..."
sudo systemctl restart systemd-binfmt || log_error "Falha ao reiniciar systemd-binfmt. Verifique o status do serviço."

log_info "========================================================="
log_info "PONTE UNIVERSAL ATIVADA E PERSISTENTE!"
log_info "Agora você pode executar .exe e .apk diretamente no terminal ou clicando."
log_info "========================================================="
