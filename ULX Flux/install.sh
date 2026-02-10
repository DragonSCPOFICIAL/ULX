#!/bin/bash

# ULX Flux - Instalador Nativo Otimizado
# Mantenedor: DragonSCPOFICIAL

APP_NAME="ulxflux"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"

echo "==============================================="
echo "   Instalador ULX Flux - Performance Máxima"
echo "==============================================="

# 1. Preparação
echo "[1/5] Preparando diretórios..."
sudo mkdir -p "$INSTALL_DIR"

# 2. Copiar arquivos (preservando estrutura)
echo "[2/5] Instalando arquivos do projeto..."
sudo cp -r ./* "$INSTALL_DIR/"

# 3. Instalar dependências do sistema
echo "[3/5] Verificando dependências (Python3, Tkinter, Pillow)..."
if command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm python python-pip tk python-pillow
elif command -v apt &> /dev/null; then
    sudo apt update && sudo apt install -y python3 python3-pip python3-tk python3-pil
else
    echo "Aviso: Distribuição não reconhecida. Instale manualmente: python3, tkinter, pillow."
fi

# 4. Configurar Executável Global
echo "[4/5] Configurando acesso global..."
sudo chmod +x "$INSTALL_DIR/ULXFlux.sh"
sudo ln -sf "$INSTALL_DIR/ULXFlux.sh" "$BIN_DIR/$APP_NAME"

# 5. Atalho de Desktop
echo "[5/5] Criando atalho no sistema..."
cat <<EOF | sudo tee "$DESKTOP_DIR/$APP_NAME.desktop" > /dev/null
[Desktop Entry]
Name=ULX Flux
Comment=Tradução Nativa de Alta Performance para Linux
Exec=$APP_NAME
Icon=$INSTALL_DIR/assets/icon.png
Terminal=false
Type=Application
Categories=Development;System;Utility;
Keywords=wine;translation;performance;ulx;
EOF

echo "==============================================="
echo "   ULX Flux instalado com sucesso!"
echo "   Execute digitando 'ulxflux' no terminal."
echo "==============================================="
