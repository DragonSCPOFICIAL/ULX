#!/bin/bash
# Script de instalação e desinstalação do ULX - "One-Click Metal Performance"

# Cores para mensagens no terminal (formato robusto para Bash)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NC=$(tput sgr0) # No Color

# Funções de log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# Função para instalar yay se não encontrado
install_yay_if_missing() {
    log_info "Verificando e instalando AUR helper (yay) se necessário..."
    if ! command -v yay &> /dev/null; then
        log_warn "AUR helper (yay) não encontrado. Tentando instalar yay..."
        sudo pacman -S --needed --noconfirm git base-devel || { log_error "Falha ao instalar dependências para o yay."; return 1; }
        git clone https://aur.archlinux.org/yay.git /tmp/yay_install || { log_error "Falha ao clonar o repositório do yay."; return 1; }
        (cd /tmp/yay_install && makepkg -si --noconfirm) || { log_error "Falha ao compilar e instalar o yay."; return 1; }
        rm -rf /tmp/yay_install
        if ! command -v yay &> /dev/null; then
            log_error "Falha crítica: Não foi possível instalar yay. Por favor, instale yay manualmente e tente novamente."
            return 1
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
    sudo pacman -Syu --needed --noconfirm cmake gcc vulkan-devel mesa lib32-mesa nasm python wine-staging git base-devel ncurses || { log_error "Falha ao instalar dependências do pacman."; return 1; }
    
    install_yay_if_missing || return 1

    log_info "Instalando pacotes do AUR (box64-git e anbox-git) via ${AUR_HELPER}..."
    ${AUR_HELPER} -S --noconfirm box64-git anbox-git || { log_error "Falha ao instalar pacotes do AUR."; return 1; }
    log_info "Todas as dependências instaladas com sucesso!"
}

# Instalar ULX e configurar a Ponte Universal
install_ulx() {
    log_info "Iniciando instalação do ULX e configuração da Ponte Universal..."
    
    log_info "Compilando e instalando o compilador ULX..."
    make build && sudo make install || { log_error "Falha ao compilar ou instalar o compilador ULX."; return 1; }
    
    log_info "Compilando e instalando o Interceptor de Hardware..."
    chmod +x ulx_integrated_setup.sh && sudo ./ulx_integrated_setup.sh || { log_error "Falha ao executar o setup do Interceptor."; return 1; }
    
    log_info "Configurando a Ponte Universal para .EXE e .APK..."
    chmod +x ulx_universal_bridge.sh && sudo ./ulx_universal_bridge.sh || { log_error "Falha ao configurar a Ponte Universal."; return 1; }
    
    log_info "Registrando tipos de arquivo no sistema..."
    sudo cp -f assets/ulx-exe.xml /usr/share/mime/packages/ulx-exe.xml || { log_error "Falha ao copiar o MIME type de .exe."; return 1; }
    sudo cp -f assets/ulx-apk.xml /usr/share/mime/packages/ulx-apk.xml || { log_error "Falha ao copiar o MIME type de .apk."; return 1; }
    sudo update-mime-database /usr/share/mime || { log_error "Falha ao atualizar o banco de dados MIME."; return 1; }
}

# Desinstalar ULX e reverter todas as configurações
uninstall_ulx() {
    log_info "Iniciando desinstalação do ULX e revertendo todas as configurações..."
    
    log_info "Removendo binários e bibliotecas do ULX..."
    sudo rm -f /usr/local/bin/ulxc /usr/local/bin/ulx-run /usr/local/bin/ulx-run-exe /usr/local/bin/ulx-run-apk
    sudo rm -rf /usr/local/lib/ulx /usr/local/share/ulx
    
    log_info "Removendo configurações de binfmt_misc..."
    sudo rm -f /etc/binfmt.d/ulx-exe.conf /etc/binfmt.d/ulx-apk.conf
    [ -f /proc/sys/fs/binfmt_misc/ulx-exe ] && echo -1 | sudo tee /proc/sys/fs/binfmt_misc/ulx-exe > /dev/null
    [ -f /proc/sys/fs/binfmt_misc/ulx-apk ] && echo -1 | sudo tee /proc/sys/fs/binfmt_misc/ulx-apk > /dev/null
    sudo systemctl restart systemd-binfmt || log_warn "Falha ao reiniciar systemd-binfmt. Pode ser necessário reiniciar manualmente."
    
    log_info "Removendo configurações de MIME types..."
    sudo rm -f /usr/share/mime/packages/ulx-exe.xml /usr/share/mime/packages/ulx-apk.xml
    sudo update-mime-database /usr/share/mime || log_warn "Falha ao atualizar banco de dados MIME. Pode ser necessário reiniciar manualmente."
    
    log_info "Limpando artefatos de build..."
    make clean

    log_info "Removendo pacotes do AUR (box64-git e anbox-git)..."
    if command -v yay &> /dev/null; then
        yay -Rns --noconfirm box64-git anbox-git || log_warn "Falha ao remover pacotes do AUR com yay. Pode ser que já não estejam instalados."
    elif command -v paru &> /dev/null; then
        paru -Rns --noconfirm box64-git anbox-git || log_warn "Falha ao remover pacotes do AUR com paru. Pode ser que já não estejam instalados."
    else
        log_warn "Nenhum AUR helper encontrado. Remova 'box64-git' e 'anbox-git' manualmente se os instalou via AUR."
    fi
    
    log_info "Desinstalação do sistema concluída."
}

# Menu principal
main() {
    echo "========================================="
    echo "     ULX - Universal Linux eXecution"
    echo "========================================="
    echo ""
    
    case "${1:-install}" in
        install)
            install_dependencies && install_ulx
            ;;
        uninstall)
            uninstall_ulx
            ;;
        *)
            log_error "Uso: $0 [install|uninstall]"
            exit 1
            ;;
    esac
}

main "$@"
