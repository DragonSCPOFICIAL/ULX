#!/bin/bash
# Script de instalação do ULX - "One-Click Metal Performance"

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

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERRO]${NC} $1"
    exit 1 # Sair em caso de erro crítico
}

# Função para instalar yay se não encontrado
install_yay_if_missing() {
    if ! command -v yay &> /dev/null; then
        log_warn "AUR helper (yay) não encontrado. Tentando instalar yay..."
        sudo pacman -S --needed --noconfirm git base-devel || log_error "Falha ao instalar dependências para AUR helper."
        git clone https://aur.archlinux.org/yay.git /tmp/yay_install || log_error "Falha ao clonar repositório yay."
        (cd /tmp/yay_install && makepkg -si --noconfirm) || log_error "Falha ao compilar e instalar yay."
        rm -rf /tmp/yay_install
        if ! command -v yay &> /dev/null; then
            log_error "Falha crítica: Não foi possível instalar yay. Por favor, instale yay manualmente e tente novamente."
        fi
        log_info "'yay' instalado com sucesso."
    else
        log_info "AUR helper 'yay' já está instalado."
    fi
    AUR_HELPER="yay"
}

# Instalação automatizada de dependências
install_dependencies() {
    log_info "Instalando dependências essenciais via pacman..."
    sudo pacman -Syu --needed --noconfirm cmake gcc vulkan-devel mesa lib32-mesa nasm python wine-staging git base-devel || log_error "Falha ao instalar dependências via pacman."
    
    install_yay_if_missing # Garante que yay esteja disponível

    log_info "Instalando pacotes do AUR (box64-git e anbox-git) via ${AUR_HELPER}..."
    ${AUR_HELPER} -S --noconfirm box64-git anbox-git || log_error "Falha ao instalar pacotes do AUR (${AUR_HELPER})."
    log_info "Todas as dependências instaladas com sucesso!"
}

# Instalar ULX e configurar a Ponte Universal
install_ulx() {
    log_info "Iniciando instalação do ULX e configuração da Ponte Universal..."
    
    # Compilar e instalar o compilador ULX
    log_info "Compilando e instalando o compilador ULX..."
    make build || log_error "Falha na compilação do ULX."
    sudo make install || log_error "Falha na instalação do compilador ULX."
    
    # Compilar e instalar o Interceptor de Hardware
    log_info "Compilando e instalando o Interceptor de Hardware..."
    chmod +x ulx_integrated_setup.sh || log_error "Falha ao definir permissões para ulx_integrated_setup.sh."
    sudo ./ulx_integrated_setup.sh || log_error "Falha na configuração do Interceptor de Hardware."
    
    # Configurar a Ponte Universal para .exe e .apk
    log_info "Configurando a Ponte Universal para .EXE e .APK..."
    chmod +x ulx_universal_bridge.sh || log_error "Falha ao definir permissões para ulx_universal_bridge.sh."
    sudo ./ulx_universal_bridge.sh || log_error "Falha na configuração da Ponte Universal."
    
    # Registrar MIME types para integração com o explorador de arquivos
    log_info "Registrando tipos de arquivo no sistema..."
    sudo cp -f assets/ulx-exe.xml /usr/share/mime/packages/ulx-exe.xml || log_error "Falha ao copiar ulx-exe.xml."
    sudo cp -f assets/ulx-apk.xml /usr/share/mime/packages/ulx-apk.xml || log_error "Falha ao copiar ulx-apk.xml."
    sudo update-mime-database /usr/share/mime || log_error "Falha ao atualizar banco de dados MIME."
    
    log_info "ULX UNIVERSAL instalado com sucesso!"
    log_info "Reinicie o sistema para que todas as alterações tenham efeito."
}

# Desinstalar ULX e reverter todas as configurações
uninstall_ulx() {
    log_info "Iniciando desinstalação do ULX e revertendo todas as configurações..."
    
    # Remover binários e bibliotecas
    log_info "Removendo binários e bibliotecas do ULX..."
    sudo rm -f /usr/local/bin/ulxc /usr/local/bin/ulx-run /usr/local/bin/ulx-run-exe /usr/local/bin/ulx-run-apk
    sudo rm -rf /usr/local/lib/ulx /usr/local/share/ulx
    
    # Remover configurações de binfmt
    log_info "Removendo configurações de binfmt_misc..."
    sudo rm -f /etc/binfmt.d/ulx-exe.conf /etc/binfmt.d/ulx-apk.conf
    # Desativar regras binfmt ativas (se existirem)
    [ -f /proc/sys/fs/binfmt_misc/ulx-exe ] && echo -1 | sudo tee /proc/sys/fs/binfmt_misc/ulx-exe > /dev/null
    [ -f /proc/sys/fs/binfmt_misc/ulx-apk ] && echo -1 | sudo tee /proc/sys/fs/binfmt_misc/ulx-apk > /dev/null
    sudo systemctl restart systemd-binfmt || log_warn "Falha ao reiniciar systemd-binfmt. Pode ser necessário reiniciar manualmente."
    
    # Remover MIME types
    log_info "Removendo configurações de MIME types..."
    sudo rm -f /usr/share/mime/packages/ulx-exe.xml /usr/share/mime/packages/ulx-apk.xml
    sudo update-mime-database /usr/share/mime || log_warn "Falha ao atualizar banco de dados MIME. Pode ser necessário reiniciar manualmente."
    
    # Limpar artefatos de build
    log_info "Limpando artefatos de build..."
    make clean

    # Remover pacotes do AUR (se instalados)
    log_info "Removendo pacotes do AUR (box64-git e anbox-git)..."
    if command -v yay &> /dev/null; then
        AUR_HELPER="yay"
    elif command -v paru &> /dev/null; then
        AUR_HELPER="paru"
    fi

    if [ -n "${AUR_HELPER}" ]; then
        ${AUR_HELPER} -R --noconfirm box64-git anbox-git || log_warn "Falha ao remover pacotes do AUR (${AUR_HELPER}). Pode ser que já não estejam instalados."
    else
        log_warn "Nenhum AUR helper encontrado. Remova 'box64-git' e 'anbox-git' manualmente se os instalou via AUR."
    fi
    
    log_info "ULX REMOVIDO COMPLETAMENTE!"
    log_info "Reinicie o sistema para garantir a remoção completa de todos os módulos e serviços."
}

# Menu principal
main() {
    echo "========================================"
    echo "     ULX - Universal Linux eXecution"
    echo "========================================"
    echo ""
    
    case "${1:-install}" in
        install)
            install_dependencies
            install_ulx
            ;;
        uninstall)
            uninstall_ulx
            ;;
        *)
            echo "Uso: $0 [install|uninstall]"
            exit 1
            ;;
    esac
}

main "$@"
