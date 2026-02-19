#!/bin/bash
# Script de instalação do ULX - "One-Click Metal Performance"

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funções de log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Instalação automatizada de dependências
install_dependencies() {
    log_info "Instalando dependências para o ecossistema ULX Universal..."
    # Atualizar pacotes e instalar dependências essenciais
    sudo pacman -Syu --needed --noconfirm cmake gcc vulkan-devel mesa lib32-mesa nasm python wine-staging box64-git anbox-git
    log_info "Dependências instaladas com sucesso!"
}

# Instalar ULX e configurar a Ponte Universal
install_ulx() {
    log_info "Instalando ULX e configurando a Ponte Universal..."
    
    # Compilar e instalar o compilador ULX
    make build && sudo make install
    
    # Compilar e instalar o Interceptor de Hardware
    chmod +x ulx_integrated_setup.sh
    ./ulx_integrated_setup.sh
    
    # Configurar a Ponte Universal para .exe e .apk
    chmod +x ulx_universal_bridge.sh
    sudo ./ulx_universal_bridge.sh
    
    # Registrar MIME types para integração com o explorador de arquivos
    log_info "Registrando tipos de arquivo no sistema..."
    sudo cp -f assets/ulx-exe.xml /usr/share/mime/packages/ulx-exe.xml
    sudo cp -f assets/ulx-apk.xml /usr/share/mime/packages/ulx-apk.xml
    sudo update-mime-database /usr/share/mime
    
    log_info "ULX UNIVERSAL instalado com sucesso!"
    log_info "Reinicie o sistema para que todas as alterações tenham efeito."
}

# Desinstalar ULX e reverter todas as configurações
uninstall_ulx() {
    log_info "Desinstalando ULX e revertendo todas as configurações..."
    
    # Remover binários e bibliotecas
    sudo rm -f /usr/local/bin/ulxc /usr/local/bin/ulx-run /usr/local/bin/ulx-run-exe /usr/local/bin/ulx-run-apk
    sudo rm -rf /usr/local/lib/ulx /usr/local/share/ulx
    
    # Remover configurações de binfmt
    sudo rm -f /etc/binfmt.d/ulx-exe.conf /etc/binfmt.d/ulx-apk.conf
    sudo systemctl restart systemd-binfmt
    
    # Remover MIME types
    sudo rm -f /usr/share/mime/packages/ulx-exe.xml /usr/share/mime/packages/ulx-apk.xml
    sudo update-mime-database /usr/share/mime
    
    make clean
    log_info "ULX REMOVIDO COMPLETAMENTE!"
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
