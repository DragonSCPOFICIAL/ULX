#!/bin/bash
# Script de Instalação/Reinstalação - ULX Notebook Monitor (ESTÁVEL)

echo "===================================================="
echo "   ULX CLEAN INSTALLER (REMOÇÃO TOTAL ATIVADA)      "
echo "===================================================="

# Pegar o caminho absoluto
BASE_DIR=$(cd "$(dirname "$0")/../.." && pwd)

# 1. LIMPEZA PROFUNDA
echo "[1/4] Removendo versão antiga de todos os diretórios..."
sudo rm -f /usr/local/bin/ulx-notebook-monitor 2>/dev/null
sudo rm -f /usr/share/applications/ulx-monitor.desktop 2>/dev/null
sudo rm -f /usr/local/bin/ulxc 2>/dev/null
sudo rm -f /usr/local/bin/clx_engine.py 2>/dev/null
rm -f ./monitor ./monitor.c 2>/dev/null

# 2. INSTALAÇÃO DO COMPILADOR
echo "[2/4] Reinstalando motor CLX..."
COMPILER_SRC="$BASE_DIR/src/compiler/clx_compiler_intelligent.py"
sudo cp "$COMPILER_SRC" /usr/local/bin/clx_engine.py
cat << EOF > /tmp/ulxc
#!/bin/bash
python3 /usr/local/bin/clx_engine.py "\$1"
EOF
sudo mv /tmp/ulxc /usr/local/bin/ulxc
sudo chmod +x /usr/local/bin/ulxc

# 3. COMPILAÇÃO
echo "[3/4] Compilando novo binário ULX/LNX..."
ulxc monitor.ulx

# 4. FINALIZAÇÃO
if [ -f "./monitor" ]; then
    echo "[4/4] Configurando atalhos e sistema..."
    sudo cp ./monitor /usr/local/bin/ulx-notebook-monitor
    
    # Criar atalho que força o terminal a ficar aberto se houver erro
    cat << EOF > /tmp/ulx-monitor.desktop
[Desktop Entry]
Name=ULX Notebook Monitor
Comment=Monitor de Sistema Nativo ULX/LNX
Exec=konsole --hold -e /usr/local/bin/ulx-notebook-monitor
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Monitor;
EOF
    sudo mv /tmp/ulx-monitor.desktop /usr/share/applications/ulx-monitor.desktop
    sudo chmod +x /usr/share/applications/ulx-monitor.desktop

    echo "----------------------------------------------------"
    echo "   REINSTALAÇÃO CONCLUÍDA COM SUCESSO!              "
    echo "   O programa agora aguarda ENTER para fechar.      "
    echo "----------------------------------------------------"
    
    # Executa a nova versão
    /usr/local/bin/ulx-notebook-monitor
else
    echo "Erro na compilação. O binário não foi gerado."
    exit 1
fi
