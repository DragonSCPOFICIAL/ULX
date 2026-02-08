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

# 2. Copiar arquivos do compilador, studio e exemplos
echo "[2/5] Copiando arquivos do ecossistema..."
sudo cp ./bin/ulxc "$INSTALL_DIR/bin/"
sudo cp ./bin/ulx-studio "$INSTALL_DIR/bin/"
sudo cp ./bin/ulx-pack "$INSTALL_DIR/bin/"
sudo cp -r ./examples "$INSTALL_DIR/"
sudo cp -r ./include "$INSTALL_DIR/"

# 3. Configurar Executáveis e Atalhos
echo "[3/5] Configurando permissões e links..."
sudo chmod +x "$INSTALL_DIR/bin/"*
sudo ln -sf "$INSTALL_DIR/bin/ulxc" "$BIN_DIR/ulxc"
sudo ln -sf "$INSTALL_DIR/bin/ulx-studio" "$BIN_DIR/ulx-studio"
sudo ln -sf "$INSTALL_DIR/bin/ulx-pack" "$BIN_DIR/ulx-pack"

# Criar atalho para o ULX Studio no menu
cat <<EOF | sudo tee /usr/share/applications/ulx-studio.desktop > /dev/null
[Desktop Entry]
Name=ULX Studio
Comment=IDE Nativa para Desenvolvimento ULX
Exec=ulx-studio
Icon=processor
Terminal=false
Type=Application
Categories=Development;IDE;
EOF

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
