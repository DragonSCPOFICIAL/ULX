#!/bin/bash
# Script de Instalação/Reinstalação Automatizada - ULX Notebook Monitor (Versão Estável)

echo "===================================================="
echo "   ULX AUTOMATED INSTALLER & REINSTALLER            "
echo "===================================================="

# Pegar o caminho absoluto de onde o script está sendo executado
BASE_DIR=$(cd "$(dirname "$0")/../.." && pwd)

# 1. Desinstalação prévia (Limpeza)
echo "[1/4] Removendo versões anteriores..."
sudo rm -f /usr/local/bin/ulx-notebook-monitor 2>/dev/null
sudo rm -f /usr/share/applications/ulx-monitor.desktop 2>/dev/null
rm -f ./monitor 2>/dev/null
rm -f ./monitor.c 2>/dev/null

# 2. Instalação do Motor de Compilação
echo "[2/4] Configurando motor de compilação CLX..."
COMPILER_SRC="$BASE_DIR/src/compiler/clx_compiler_intelligent.py"

if [ ! -f "$COMPILER_SRC" ]; then
    echo "Erro: Compilador não encontrado em $COMPILER_SRC"
    exit 1
fi

sudo cp "$COMPILER_SRC" /usr/local/bin/clx_engine.py
cat << EOF > /tmp/ulxc
#!/bin/bash
python3 /usr/local/bin/clx_engine.py "\$1"
EOF
sudo mv /tmp/ulxc /usr/local/bin/ulxc
sudo chmod +x /usr/local/bin/ulxc

# 3. Compilação Nativa Estável
echo "[3/4] Compilando aplicativo nativamente (Modo Estável)..."
ulxc monitor.ulx

# 4. Entrega e Configuração do Atalho
if [ -f "./monitor" ]; then
    echo "[4/4] Instalando binário e criando atalho de aplicativo..."
    sudo cp ./monitor /usr/local/bin/ulx-notebook-monitor
    
    # Instalar o atalho .desktop para aparecer no menu de aplicativos
    if [ -f "./ulx-monitor.desktop" ]; then
        sudo cp ./ulx-monitor.desktop /usr/share/applications/
        sudo chmod +x /usr/share/applications/ulx-monitor.desktop
    fi

    echo "----------------------------------------------------"
    echo "   INSTALAÇÃO CONCLUÍDA COM SUCESSO!                "
    echo "   Comando: ulx-notebook-monitor                    "
    echo "   Ou procure por 'ULX Notebook Monitor' no seu menu"
    echo "----------------------------------------------------"
    
    # Executa uma vez para mostrar o resultado
    ulx-notebook-monitor
else
    echo "Erro fatal na compilação. O binário não foi gerado."
    exit 1
fi
