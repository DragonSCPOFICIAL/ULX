#!/bin/bash

APP_NAME="ulx"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"

echo "==============================================="
echo "   Iniciando Instalação da ULX"
echo "==============================================="

# 1. Criar diretórios
echo "[1/4] Criando diretórios do sistema..."
sudo mkdir -p "$INSTALL_DIR/src"
sudo mkdir -p "$INSTALL_DIR/bin"

# 2. Copiar arquivos
echo "[2/4] Copiando arquivos da linguagem..."
sudo cp -r ./src/* "$INSTALL_DIR/src/"
sudo cp -r ./bin/* "$INSTALL_DIR/bin/"

# 3. Instalar dependências
echo "[3/4] Verificando dependências do sistema (Python3 e GCC)..."
if command -v pacman &> /dev/null; then
    # Arch Linux
    sudo pacman -S --noconfirm python gcc
elif command -v apt &> /dev/null; then
    # Debian/Ubuntu
    sudo apt update && sudo apt install -y python3 gcc
else
    echo "Aviso: Gerenciador de pacotes não reconhecido. Certifique-se de ter Python3 e GCC instalados."
fi

# 4. Configurar Executável
echo "[4/4] Configurando permissões e links..."
sudo chmod +x "$INSTALL_DIR/bin/dragon"
sudo ln -sf "$INSTALL_DIR/bin/dragon" "$BIN_DIR/dragon"

echo "==============================================="
echo "        Instalação Concluída com Sucesso!"
echo "==============================================="
echo "Você pode usar o compilador 'dragon' agora. Tente 'dragon --help' ou 'dragon examples/ola_mundo.dl'"
