#!/bin/bash

APP_NAME="ulx"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"

echo "==============================================="
echo "   Iniciando Instalação do Ecossistema ULX"
echo "==============================================="

# 1. Criar diretórios
echo "[1/5] Criando diretórios do sistema..."
sudo mkdir -p "$INSTALL_DIR/bin"
sudo mkdir -p "$INSTALL_DIR/src/compiler"
sudo mkdir -p "$INSTALL_DIR/examples"

# 2. Copiar arquivos do compilador e exemplos
echo "[2/5] Copiando arquivos do compilador e exemplos..."
sudo cp ./bin/ulxc "$INSTALL_DIR/bin/"
sudo cp ./examples/hello.ulx "$INSTALL_DIR/examples/"
sudo cp ./src/compiler/main.c "$INSTALL_DIR/src/compiler/"

# 3. Configurar Executável
echo "[3/5] Configurando permissões e links..."
sudo chmod +x "$INSTALL_DIR/bin/ulxc"
sudo ln -sf "$INSTALL_DIR/bin/ulxc" "$BIN_DIR/ulxc"

# 4. Integração de Sistema (MIME Types e Handlers)
echo "[4/5] Integrando ULX ao sistema operacional..."
sudo chmod +x ./src/ulx-integrator.sh
sudo ./src/ulx-integrator.sh

# 5. Verificar dependências de sistema (GCC, Unzip) e instalar se necessário
echo "[5/5] Verificando dependências de sistema..."

# Verificar GCC
if ! command -v gcc &> /dev/null; then
    echo "GCC não encontrado. Instalando..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm gcc
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y gcc
    fi
fi

# Verificar Unzip
if ! command -v unzip &> /dev/null; then
    echo "Unzip não encontrado. Instalando..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm unzip
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y unzip
    fi
fi

echo "==============================================="
echo "        Instalação Concluída com Sucesso!"
echo "==============================================="
echo "Você pode usar o compilador 'ulxc' agora. Tente 'ulxc /opt/ulx/examples/hello.ulx'"
