#!/bin/bash

# ULX Flux - Instalador Nativo (Baseado no modelo AetherLauncher)
# Mantenedor: DragonSCPOFICIAL
# Descrição: Camada de tradução para linguagem ULX no Linux

APP_NAME="ulxflux"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"

echo "==============================================="
echo "   Iniciando Instalação do ULX Flux"
echo "   (Tradução Nativa via Linguagem ULX)"
echo "==============================================="

# 1. Criar diretórios
echo "[1/5] Criando diretórios do sistema..."
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR/src"
sudo mkdir -p "$INSTALL_DIR/bin"

# 2. Copiar arquivos
echo "[2/5] Copiando arquivos do projeto..."
sudo cp -r ./* "$INSTALL_DIR/"

# 3. Instalar dependências
echo "[3/5] Verificando dependências do sistema..."
if command -v pacman &> /dev/null; then
    # Arch Linux
    sudo pacman -S --noconfirm python python-pip python-pillow tk
elif command -v apt &> /dev/null; then
    # Debian/Ubuntu
    sudo apt update && sudo apt install -y python3 python3-pip python3-pil python3-tk
else
    echo "Aviso: Gerenciador de pacotes não reconhecido. Certifique-se de ter Python3 e Tkinter instalados."
fi

# 4. Configurar Executável
echo "[4/5] Configurando permissões e links..."
sudo chmod +x "$INSTALL_DIR/ULXFlux.sh"
sudo ln -sf "$INSTALL_DIR/ULXFlux.sh" "$BIN_DIR/$APP_NAME"

# 5. Criar atalho no menu
echo "[5/5] Criando atalho no menu de aplicativos..."
cat <<EOF | sudo tee "$DESKTOP_DIR/$APP_NAME.desktop" > /dev/null
[Desktop Entry]
Name=ULX Flux
Comment=Tradutor de Aplicações para Linguagem ULX (Nativo)
Exec=$APP_NAME
Icon=$INSTALL_DIR/assets/icon.png
Terminal=false
Type=Application
Categories=Development;System;
EOF

echo "==============================================="
echo "        Instalação Concluída com Sucesso!"
echo "==============================================="
echo "Você pode abrir o tradutor digitando '$APP_NAME' ou pelo menu."
