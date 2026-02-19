#!/bin/bash
# Script de instalação e desinstalação do ULX - "One-Click Metal Performance"
# Versão 2.0 — Suporte multi-distro, multi-AUR-helper, patch automático de build

set -euo pipefail

# ─── Cores ───────────────────────────────────────────────────────────────────
RED=$(tput setaf 1 2>/dev/null || echo "")
GREEN=$(tput setaf 2 2>/dev/null || echo "")
YELLOW=$(tput setaf 3 2>/dev/null || echo "")
CYAN=$(tput setaf 6 2>/dev/null || echo "")
BOLD=$(tput bold 2>/dev/null || echo "")
NC=$(tput sgr0 2>/dev/null || echo "")

# ─── Log ─────────────────────────────────────────────────────────────────────
log_info()    { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()    { echo -e "${YELLOW}[AVISO]${NC} $1"; }
log_error()   { echo -e "${RED}[ERRO]${NC}  $1" >&2; }
log_step()    { echo -e "\n${CYAN}${BOLD}══ $1 ══${NC}"; }
log_success() { echo -e "${GREEN}${BOLD}✔ $1${NC}"; }

# ─── Rastreamento de erros ────────────────────────────────────────────────────
FAILED_STEPS=()

record_error() {
    FAILED_STEPS+=("$1")
    log_error "$1"
}

print_error_summary() {
    if [ ${#FAILED_STEPS[@]} -gt 0 ]; then
        echo ""
        log_error "══════════════════════════════════════"
        log_error " RESUMO DE FALHAS (${#FAILED_STEPS[@]} etapa(s)):"
        for step in "${FAILED_STEPS[@]}"; do
            log_error "  • $step"
        done
        log_error "══════════════════════════════════════"
        return 1
    fi
    return 0
}

# ─── Detectar usuário real ────────────────────────────────────────────────────
get_real_user() {
    if [ -n "${SUDO_USER:-}" ]; then
        echo "$SUDO_USER"
    else
        echo "$USER"
    fi
}

run_as_user() {
    local real_user
    real_user=$(get_real_user)
    sudo -u "$real_user" "$@"
}

get_home_dir() {
    local real_user
    real_user=$(get_real_user)
    eval echo "~$real_user"
}

# ─── Detectar distro ──────────────────────────────────────────────────────────
detect_distro() {
    if [ -f /etc/os-release ]; then
        # shellcheck disable=SC1091
        . /etc/os-release
        DISTRO_ID="${ID:-unknown}"
        DISTRO_LIKE="${ID_LIKE:-}"
    else
        DISTRO_ID="unknown"
        DISTRO_LIKE=""
    fi

    # Família da distro
    if echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE "arch|manjaro|endeavour|garuda|artix"; then
        DISTRO_FAMILY="arch"
    elif echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE "debian|ubuntu|mint|pop|kali|elementary"; then
        DISTRO_FAMILY="debian"
    elif echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE "fedora|rhel|centos|rocky|alma"; then
        DISTRO_FAMILY="fedora"
    elif echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE "opensuse|suse"; then
        DISTRO_FAMILY="suse"
    else
        DISTRO_FAMILY="unknown"
    fi

    log_info "Distro detectada: ${DISTRO_ID} (família: ${DISTRO_FAMILY})"
}

# ─── Gerenciador de pacotes ───────────────────────────────────────────────────
PKG_INSTALL=""

setup_pkg_manager() {
    case "$DISTRO_FAMILY" in
        arch)
            PKG_INSTALL="pacman -S --needed --noconfirm"
            PKG_UPDATE="pacman -Syu --noconfirm"
            ;;
        debian)
            PKG_INSTALL="apt-get install -y"
            PKG_UPDATE="apt-get update && apt-get upgrade -y"
            ;;
        fedora)
            PKG_INSTALL="dnf install -y"
            PKG_UPDATE="dnf upgrade -y"
            ;;
        suse)
            PKG_INSTALL="zypper install -y"
            PKG_UPDATE="zypper update -y"
            ;;
        *)
            log_warn "Distro não reconhecida. Assumindo pacman (Arch). Ajuste manualmente se necessário."
            PKG_INSTALL="pacman -S --needed --noconfirm"
            PKG_UPDATE="pacman -Syu --noconfirm"
            ;;
    esac
}

pkg_install() {
    # shellcheck disable=SC2086
    eval "$PKG_INSTALL $*"
}

# ─── Verificar AUR helpers ────────────────────────────────────────────────────
AUR_HELPER=""
AUR_HELPERS_PRIORITY=("yay" "paru" "trizen" "pikaur")

find_aur_helper() {
    local home_dir
    home_dir=$(get_home_dir)
    local real_user
    real_user=$(get_real_user)

    for helper in "${AUR_HELPERS_PRIORITY[@]}"; do
        for bin in \
            "/usr/bin/$helper" \
            "/usr/local/bin/$helper" \
            "$home_dir/.local/bin/$helper" \
            "$home_dir/go/bin/$helper"
        do
            if [ -x "$bin" ]; then
                AUR_HELPER="$bin"
                log_info "AUR helper encontrado: $AUR_HELPER"
                return 0
            fi
        done
        # Fallback via which
        if sudo -u "$real_user" bash -c "which $helper" &>/dev/null; then
            AUR_HELPER="$helper"
            log_info "AUR helper encontrado via PATH: $AUR_HELPER"
            return 0
        fi
    done

    return 1
}

install_yay() {
    local real_user
    real_user=$(get_real_user)
    local build_dir="/tmp/yay_install_$$"

    log_info "Instalando dependências para compilar yay..."
    pacman -S --needed --noconfirm git base-devel \
        || { record_error "Falha ao instalar dependências do yay"; return 1; }

    log_info "Clonando repositório do yay..."
    sudo -u "$real_user" git clone https://aur.archlinux.org/yay.git "$build_dir" \
        || { record_error "Falha ao clonar yay"; return 1; }

    log_info "Compilando e instalando yay..."
    (cd "$build_dir" && sudo -u "$real_user" makepkg -si --noconfirm) \
        || { record_error "Falha ao compilar yay"; rm -rf "$build_dir"; return 1; }

    rm -rf "$build_dir"
    AUR_HELPER="yay"
    log_success "yay instalado com sucesso."
}

install_paru() {
    local real_user
    real_user=$(get_real_user)
    local build_dir="/tmp/paru_install_$$"

    log_info "Instalando dependências para compilar paru..."
    pacman -S --needed --noconfirm git base-devel rust \
        || { record_error "Falha ao instalar dependências do paru"; return 1; }

    log_info "Clonando repositório do paru..."
    sudo -u "$real_user" git clone https://aur.archlinux.org/paru.git "$build_dir" \
        || { record_error "Falha ao clonar paru"; return 1; }

    log_info "Compilando e instalando paru..."
    (cd "$build_dir" && sudo -u "$real_user" makepkg -si --noconfirm) \
        || { record_error "Falha ao compilar paru"; rm -rf "$build_dir"; return 1; }

    rm -rf "$build_dir"
    AUR_HELPER="paru"
    log_success "paru instalado com sucesso."
}

ensure_aur_helper() {
    if [ "$DISTRO_FAMILY" != "arch" ]; then
        log_warn "AUR helper só é necessário em sistemas Arch. Pulando."
        return 0
    fi

    if find_aur_helper; then
        return 0
    fi

    log_warn "Nenhum AUR helper encontrado. Tentando instalar yay..."
    install_yay && return 0

    log_warn "Falha ao instalar yay. Tentando instalar paru como alternativa..."
    install_paru && return 0

    record_error "Nenhum AUR helper pôde ser instalado (yay, paru)."
    return 1
}

aur_install() {
    if [ -z "$AUR_HELPER" ]; then
        record_error "AUR helper não disponível para instalar: $*"
        return 1
    fi
    run_as_user "$AUR_HELPER" -S --noconfirm "$@"
}

aur_remove() {
    if [ -z "$AUR_HELPER" ]; then
        log_warn "AUR helper não disponível. Remova manualmente: $*"
        return 0
    fi
    run_as_user "$AUR_HELPER" -Rns --noconfirm "$@" \
        || log_warn "Falha ao remover via AUR helper (talvez já removido): $*"
}

# ─── Patch automático: corrigir use-after-free no ulx_vulkan_layer.cpp ────────
patch_vulkan_use_after_free() {
    local file="gpu/ulx_vulkan_layer.cpp"

    if [ ! -f "$file" ]; then
        log_warn "Arquivo '$file' não encontrado. Pulando patch de use-after-free."
        return 0
    fi

    # Verifica se o padrão problemático existe: uso de variável após free()
    # Padrão genérico: free(X) seguido de uso de X antes de atribuição nova
    if grep -n "free(" "$file" | grep -q "ptr"; then
        log_info "Aplicando patch de use-after-free em '$file'..."

        # Cria backup
        cp "$file" "${file}.bak"

        # Substitui padrões comuns de use-after-free:
        # free(ptr);  →  free(ptr); ptr = nullptr;
        # Aplica apenas onde ainda não há "ptr = null" na linha seguinte
        python3 - "$file" <<'PYEOF'
import re, sys

path = sys.argv[1]
with open(path, "r") as f:
    lines = f.readlines()

fixed = []
i = 0
while i < len(lines):
    fixed.append(lines[i])
    # Detecta linha com free(alguma_variavel);
    m = re.match(r'^(\s*)free\((\w+)\);', lines[i])
    if m:
        indent = m.group(1)
        var = m.group(2)
        # Verifica se a próxima linha já anula o ponteiro
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if not re.match(rf'^\s*{re.escape(var)}\s*=\s*(nullptr|NULL|0)\s*;', next_line):
            fixed.append(f"{indent}{var} = nullptr;  // patch: evitar use-after-free\n")
    i += 1

with open(path, "w") as f:
    f.writelines(fixed)

print(f"Patch aplicado: {path}")
PYEOF
        log_success "Patch de use-after-free aplicado em '$file' (backup: ${file}.bak)."
    else
        log_info "Nenhum padrão de use-after-free detectado em '$file'. Nenhuma alteração necessária."
    fi
}

# ─── Instalar dependências ────────────────────────────────────────────────────
install_dependencies() {
    log_step "Instalando Dependências"

    detect_distro
    setup_pkg_manager

    case "$DISTRO_FAMILY" in
        arch)
            # Resolve conflito wine / wine-staging
            if pacman -Qq wine &>/dev/null && ! pacman -Qq wine-staging &>/dev/null; then
                log_warn "Removendo 'wine' para instalar 'wine-staging'..."
                pacman -Rns --noconfirm wine \
                    || { record_error "Falha ao remover 'wine'"; return 1; }
            fi

            pacman -Syu --needed --noconfirm \
                cmake gcc vulkan-headers vulkan-icd-loader \
                mesa lib32-mesa vulkan-tools \
                nasm python git base-devel ncurses \
                wine-staging \
                || { record_error "Falha ao instalar dependências (pacman)"; return 1; }

            ensure_aur_helper || return 1

            log_info "Instalando pacotes do AUR: box64-git..."
            aur_install box64-git \
                || { record_error "Falha ao instalar box64-git via AUR"; return 1; }
            ;;

        debian)
            apt-get update -y || log_warn "apt-get update falhou, tentando continuar..."
            apt-get install -y \
                cmake gcc g++ libvulkan-dev mesa-vulkan-drivers \
                nasm python3 git build-essential libncurses-dev \
                wine \
                || { record_error "Falha ao instalar dependências (apt)"; return 1; }
            log_warn "box64 não é empacotado oficialmente para Debian/Ubuntu. Instale manualmente."
            ;;

        fedora)
            dnf install -y \
                cmake gcc gcc-c++ vulkan-devel mesa-vulkan-drivers \
                nasm python3 git ncurses-devel \
                wine \
                || { record_error "Falha ao instalar dependências (dnf)"; return 1; }
            log_warn "box64 pode não estar disponível via dnf. Verifique o repositório do projeto."
            ;;

        suse)
            zypper install -y \
                cmake gcc gcc-c++ vulkan-devel Mesa-vulkan-drivers \
                nasm python3 git ncurses-devel \
                wine \
                || { record_error "Falha ao instalar dependências (zypper)"; return 1; }
            log_warn "box64 pode não estar disponível via zypper. Verifique o repositório do projeto."
            ;;

        *)
            record_error "Família de distro desconhecida. Instale as dependências manualmente."
            return 1
            ;;
    esac

    log_success "Dependências instaladas."
}

# ─── Compilar e instalar ULX ──────────────────────────────────────────────────
install_ulx() {
    log_step "Compilando e Instalando ULX"

    # Aplica patch antes de compilar
    patch_vulkan_use_after_free

    log_info "Compilando ULX (make build)..."
    make build \
        || { record_error "Falha no 'make build'"; return 1; }

    log_info "Instalando ULX (make install)..."
    make install \
        || { record_error "Falha no 'make install'"; return 1; }

    log_info "Executando setup do Interceptor de Hardware..."
    if [ -f ulx_integrated_setup.sh ]; then
        chmod +x ulx_integrated_setup.sh
        ./ulx_integrated_setup.sh \
            || { record_error "Falha no ulx_integrated_setup.sh"; return 1; }
    else
        record_error "ulx_integrated_setup.sh não encontrado."
        return 1
    fi

    log_info "Configurando Ponte Universal (.EXE / .APK)..."
    if [ -f ulx_universal_bridge.sh ]; then
        chmod +x ulx_universal_bridge.sh
        ./ulx_universal_bridge.sh \
            || { record_error "Falha no ulx_universal_bridge.sh"; return 1; }
    else
        record_error "ulx_universal_bridge.sh não encontrado."
        return 1
    fi

    log_info "Registrando MIME types..."
    for mime_file in ulx-exe ulx-apk; do
        local src="assets/${mime_file}.xml"
        local dst="/usr/share/mime/packages/${mime_file}.xml"
        if [ -f "$src" ]; then
            cp -f "$src" "$dst" \
                || { record_error "Falha ao copiar ${mime_file}.xml"; return 1; }
        else
            record_error "Arquivo de MIME não encontrado: $src"
            return 1
        fi
    done

    update-mime-database /usr/share/mime \
        || { record_error "Falha ao atualizar banco de dados MIME"; return 1; }

    log_success "ULX instalado com sucesso!"
}

# ─── Desinstalar ULX ──────────────────────────────────────────────────────────
uninstall_ulx() {
    log_step "Desinstalando ULX"

    log_info "Removendo binários e bibliotecas..."
    rm -f /usr/local/bin/ulxc \
          /usr/local/bin/ulx-run \
          /usr/local/bin/ulx-run-exe \
          /usr/local/bin/ulx-run-apk
    rm -rf /usr/local/lib/ulx /usr/local/share/ulx

    log_info "Removendo configurações de binfmt_misc..."
    for fmt in ulx-exe ulx-apk; do
        rm -f "/etc/binfmt.d/${fmt}.conf"
        if [ -f "/proc/sys/fs/binfmt_misc/${fmt}" ]; then
            echo -1 | tee "/proc/sys/fs/binfmt_misc/${fmt}" > /dev/null \
                || log_warn "Falha ao desregistrar binfmt: $fmt"
        fi
    done

    if systemctl is-active --quiet systemd-binfmt; then
        systemctl restart systemd-binfmt \
            || log_warn "Falha ao reiniciar systemd-binfmt. Reinicie o sistema se necessário."
    fi

    log_info "Removendo MIME types..."
    rm -f /usr/share/mime/packages/ulx-exe.xml \
          /usr/share/mime/packages/ulx-apk.xml
    update-mime-database /usr/share/mime \
        || log_warn "Falha ao atualizar banco de dados MIME."

    log_info "Limpando artefatos de build..."
    [ -f Makefile ] && make clean || log_warn "Makefile não encontrado, pulando 'make clean'."

    log_info "Removendo pacotes AUR (box64-git)..."
    detect_distro
    if [ "$DISTRO_FAMILY" = "arch" ]; then
        find_aur_helper && aur_remove box64-git \
            || log_warn "AUR helper não encontrado. Remova 'box64-git' manualmente."
    fi

    log_success "Desinstalação concluída."
}

# ─── Verificar privilégios ────────────────────────────────────────────────────
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "Execute este script como root: sudo $0 [install|uninstall]"
        exit 1
    fi
    if [ -z "${SUDO_USER:-}" ]; then
        log_error "Use 'sudo' (não faça login direto como root)."
        log_error "Motivo: algumas etapas precisam ser executadas como usuário normal."
        log_error "Uso: sudo $0 [install|uninstall]"
        exit 1
    fi
}

# ─── Ajuda ────────────────────────────────────────────────────────────────────
show_help() {
    echo ""
    echo "  Uso: sudo $0 [OPÇÃO]"
    echo ""
    echo "  Opções:"
    echo "    install     Instala dependências e o ULX (padrão)"
    echo "    uninstall   Remove o ULX e suas configurações"
    echo "    help        Exibe esta ajuda"
    echo ""
    echo "  Distros suportadas: Arch Linux, Manjaro, Debian, Ubuntu, Fedora, openSUSE"
    echo "  AUR helpers suportados: yay, paru, trizen, pikaur (instalação automática de yay/paru)"
    echo ""
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
    echo ""
    echo "${CYAN}${BOLD}╔═══════════════════════════════════════╗${NC}"
    echo "${CYAN}${BOLD}║   ULX - Universal Linux eXecution     ║${NC}"
    echo "${CYAN}${BOLD}║         One-Click Metal Performance   ║${NC}"
    echo "${CYAN}${BOLD}╚═══════════════════════════════════════╝${NC}"
    echo ""

    check_root

    case "${1:-install}" in
        install)
            install_dependencies && install_ulx
            ;;
        uninstall)
            uninstall_ulx
            ;;
        help|--help|-h)
            show_help
            exit 0
            ;;
        *)
            log_error "Opção inválida: '${1}'"
            show_help
            exit 1
            ;;
    esac

    # Resumo final
    if ! print_error_summary; then
        echo ""
        log_error "A operação concluiu com erros. Revise as mensagens acima."
        read -rp "Pressione ENTER para fechar..."
        exit 1
    fi
}

# Captura erros não tratados pelo set -e
trap 'log_error "Erro inesperado na linha $LINENO. Saindo."; exit 1' ERR

main "$@"
