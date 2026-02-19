#!/bin/bash
# Script de instalação e desinstalação do ULX - "One-Click Metal Performance"

# Cores para mensagens no terminal
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NC=$(tput sgr0)

# Funções de log
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERRO]${NC} $1"; }

# ─── Detectar usuário real (mesmo quando rodando via sudo) ───────────────────
get_real_user() {
    if [ -n "$SUDO_USER" ]; then
        echo "$SUDO_USER"
    else
        echo "$USER"
    fi
}

# Executa um comando como o usuário real (não root)
run_as_user() {
    local real_user
    real_user=$(get_real_user)
    sudo -u "$real_user" "$@"
}

# ─── Instalar yay se não encontrado ─────────────────────────────────────────
install_yay_if_missing() {
    log_info "Verificando e instalando AUR helper (yay) se necessário..."

    # Verifica tanto para root quanto para o usuário real
    local real_user
    real_user=$(get_real_user)

    if sudo -u "$real_user" command -v yay &> /dev/null; then
        log_info "AUR helper 'yay' já está instalado."
        AUR_HELPER="yay"
        return 0
    fi

    log_warn "AUR helper (yay) não encontrado. Tentando instalar yay..."

    pacman -S --needed --noconfirm git base-devel \
        || { log_error "Falha ao instalar dependências para o yay."; return 1; }

    # Clone e build como usuário normal — makepkg NÃO pode rodar como root
    local build_dir="/tmp/yay_install_$$"
    sudo -u "$real_user" git clone https://aur.archlinux.org/yay.git "$build_dir" \
        || { log_error "Falha ao clonar o repositório do yay."; return 1; }

    (cd "$build_dir" && sudo -u "$real_user" makepkg -si --noconfirm) \
        || { log_error "Falha ao compilar e instalar o yay."; rm -rf "$build_dir"; return 1; }

    rm -rf "$build_dir"

    if ! sudo -u "$real_user" command -v yay &> /dev/null; then
        log_error "Falha crítica: Não foi possível instalar yay. Instale manualmente e tente novamente."
        return 1
    fi

    log_info "'yay' instalado com sucesso."
    AUR_HELPER="yay"
}

# ─── Instalar dependências ───────────────────────────────────────────────────
install_dependencies() {
    log_info "Instalando dependências essenciais via pacman..."

    # Resolver conflito entre wine e wine-staging
    # Verifica se 'wine' (versão padrão) está instalado E se wine-staging NÃO está
    if pacman -Qq wine &> /dev/null && ! pacman -Qq wine-staging &> /dev/null; then
        log_warn "Conflito detectado: 'wine' instalado. Removendo para instalar 'wine-staging'..."
        pacman -Rns --noconfirm wine \
            || { log_error "Falha ao remover 'wine'."; return 1; }
    elif pacman -Qq wine-staging &> /dev/null; then
        log_info "'wine-staging' já está instalado. Nenhuma ação necessária."
    else
        log_info "Nenhuma versão de wine instalada. Prosseguindo com a instalação de 'wine-staging'."
    fi

    pacman -Syu --needed --noconfirm \
        cmake gcc vulkan-devel mesa lib32-mesa nasm python \
        wine-staging git base-devel ncurses \
        || { log_error "Falha ao instalar dependências do pacman."; return 1; }

    install_yay_if_missing || return 1

    # box64 está disponível como 'box64' no AUR; anbox-git foi removido do AUR.
    # Ajuste a lista de pacotes conforme sua necessidade real.
    local aur_packages=("box64-git")

    log_info "Instalando pacotes do AUR via ${AUR_HELPER}: ${aur_packages[*]}..."

    # yay/makepkg DEVE ser executado como usuário normal
    run_as_user "$AUR_HELPER" -S --noconfirm "${aur_packages[@]}" \
        || { log_error "Falha ao instalar pacotes do AUR."; return 1; }

    log_info "Todas as dependências instaladas com sucesso!"
}

# ─── Instalar ULX ────────────────────────────────────────────────────────────
install_ulx() {
    log_info "Iniciando instalação do ULX e configuração da Ponte Universal..."

    log_info "Compilando e instalando o compilador ULX..."
    make build && make install \
        || { log_error "Falha ao compilar ou instalar o compilador ULX."; return 1; }

    log_info "Compilando e instalando o Interceptor de Hardware..."
    chmod +x ulx_integrated_setup.sh && ./ulx_integrated_setup.sh \
        || { log_error "Falha ao executar o setup do Interceptor."; return 1; }

    log_info "Configurando a Ponte Universal para .EXE e .APK..."
    chmod +x ulx_universal_bridge.sh && ./ulx_universal_bridge.sh \
        || { log_error "Falha ao configurar a Ponte Universal."; return 1; }

    log_info "Registrando tipos de arquivo no sistema..."
    cp -f assets/ulx-exe.xml /usr/share/mime/packages/ulx-exe.xml \
        || { log_error "Falha ao copiar MIME type de .exe."; return 1; }
    cp -f assets/ulx-apk.xml /usr/share/mime/packages/ulx-apk.xml \
        || { log_error "Falha ao copiar MIME type de .apk."; return 1; }
    update-mime-database /usr/share/mime \
        || { log_error "Falha ao atualizar banco de dados MIME."; return 1; }

    log_info "ULX instalado com sucesso!"
}

# ─── Desinstalar ULX ─────────────────────────────────────────────────────────
uninstall_ulx() {
    log_info "Iniciando desinstalação do ULX..."

    log_info "Removendo binários e bibliotecas do ULX..."
    rm -f /usr/local/bin/ulxc /usr/local/bin/ulx-run \
          /usr/local/bin/ulx-run-exe /usr/local/bin/ulx-run-apk
    rm -rf /usr/local/lib/ulx /usr/local/share/ulx

    log_info "Removendo configurações de binfmt_misc..."
    rm -f /etc/binfmt.d/ulx-exe.conf /etc/binfmt.d/ulx-apk.conf
    [ -f /proc/sys/fs/binfmt_misc/ulx-exe ] \
        && echo -1 | tee /proc/sys/fs/binfmt_misc/ulx-exe > /dev/null
    [ -f /proc/sys/fs/binfmt_misc/ulx-apk ] \
        && echo -1 | tee /proc/sys/fs/binfmt_misc/ulx-apk > /dev/null
    systemctl restart systemd-binfmt \
        || log_warn "Falha ao reiniciar systemd-binfmt. Reinicie manualmente se necessário."

    log_info "Removendo MIME types..."
    rm -f /usr/share/mime/packages/ulx-exe.xml /usr/share/mime/packages/ulx-apk.xml
    update-mime-database /usr/share/mime \
        || log_warn "Falha ao atualizar banco de dados MIME."

    log_info "Limpando artefatos de build..."
    make clean

    log_info "Removendo pacotes do AUR..."
    local real_user
    real_user=$(get_real_user)

    if sudo -u "$real_user" command -v yay &> /dev/null; then
        # yay também não pode rodar como root
        run_as_user yay -Rns --noconfirm box64-git \
            || log_warn "Falha ao remover pacotes do AUR. Talvez já não estejam instalados."
    elif sudo -u "$real_user" command -v paru &> /dev/null; then
        run_as_user paru -Rns --noconfirm box64-git \
            || log_warn "Falha ao remover pacotes do AUR."
    else
        log_warn "Nenhum AUR helper encontrado. Remova 'box64-git' manualmente se necessário."
    fi

    log_info "Desinstalação concluída."
}

# ─── Verificar privilégios ───────────────────────────────────────────────────
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "Este script precisa ser executado como root (use sudo)."
        exit 1
    fi
    if [ -z "$SUDO_USER" ]; then
        log_error "Execute com 'sudo' (não diretamente como root), para que o usuário real seja detectado."
        log_error "Uso: sudo $0 [install|uninstall]"
        exit 1
    fi
}

# ─── Menu principal ──────────────────────────────────────────────────────────
main() {
    echo "========================================="
    echo "     ULX - Universal Linux eXecution"
    echo "========================================="
    echo ""

    check_root

    case "${1:-install}" in
        install)
            install_dependencies && install_ulx
            ;;
        uninstall)
            uninstall_ulx
            ;;
        *)
            log_error "Uso: sudo $0 [install|uninstall]"
            exit 1
            ;;
    esac
}

main "$@"

# Mantém o terminal aberto em caso de erro para análise
if [ $? -ne 0 ]; then
    log_error "A instalação falhou. Verifique as mensagens acima."
    log_info "O terminal permanecerá aberto para você analisar o erro."
    read -rp "Pressione ENTER para fechar..."
fi
