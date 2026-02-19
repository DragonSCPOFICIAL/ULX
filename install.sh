#!/bin/bash
# Script de instalação do ULX

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

# Verificar dependências
check_dependencies() {
    log_info "Verificando dependências..."
    
    # Python 3
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 não encontrado. Por favor, instale Python 3.8+"
        exit 1
    fi
    
    # GCC
    if ! command -v gcc &> /dev/null; then
        log_warn "GCC não encontrado. O compilador usará modo interpretado."
    fi
    
    # NASM (opcional)
    if ! command -v nasm &> /dev/null; then
        log_warn "NASM não encontrado. Syscalls diretas não estarão disponíveis."
    fi
    
    log_info "Dependências verificadas!"
}

# Instalar ULX
install_ulx() {
    log_info "Instalando ULX..."
    
    # Diretório de instalação
    PREFIX=${PREFIX:-/usr/local}
    
    # Criar diretórios
    sudo mkdir -p "$PREFIX/bin"
    sudo mkdir -p "$PREFIX/lib/ulx"
    sudo mkdir -p "$PREFIX/share/ulx/examples"
    
    # Instalar compilador
    log_info "Instalando compilador..."
    sudo cp src/compiler/ulxc.py "$PREFIX/bin/ulxc"
    sudo chmod +x "$PREFIX/bin/ulxc"
    
    # Instalar módulos
    log_info "Instalando módulos..."
    sudo cp -r src "$PREFIX/lib/ulx/"
    sudo cp -r core "$PREFIX/lib/ulx/"
    
 # 3. Instalar exemplos
    log_info "Instalando exemplos..."
    sudo cp -r examples/* "$PREFIX/share/ulx/examples/"
    
    # Instalar documentação
    log_info "Instalando documentação..."
    sudo cp README.md "$PREFIX/share/ulx/"

    # 4. Configurar Ponte Universal (.EXE & .APK)
    log_info "Configurando suporte nativo para .EXE e .APK..."
    if [ -f "./ulx_universal_bridge.sh" ]; then
        chmod +x ./ulx_universal_bridge.sh
        sudo ./ulx_universal_bridge.sh
    fi
    
    log_info "ULX instalado com sucesso!"
    log_info "Use 'ulxc --help' para ver as opções"
}

# Desinstalar ULX
uninstall_ulx() {
    log_info "Desinstalando ULX..."
    
    PREFIX=${PREFIX:-/usr/local}
    
    sudo rm -f "$PREFIX/bin/ulxc"
    sudo rm -f "$PREFIX/bin/ulx-*"
    sudo rm -rf "$PREFIX/lib/ulx"
    sudo rm -rf "$PREFIX/share/ulx"
    
    log_info "ULX desinstalado!"
}

# Menu principal
main() {
    echo "========================================"
    echo "     ULX - Universal Linux eXecution"
    echo "========================================"
    echo ""
    
    case "${1:-install}" in
        install)
            check_dependencies
            install_ulx
            ;;
        uninstall)
            uninstall_ulx
            ;;
        reinstall)
            uninstall_ulx
            check_dependencies
            install_ulx
            ;;
        *)
            echo "Uso: $0 [install|uninstall|reinstall]"
            exit 1
            ;;
    esac
}

main "$@"
