#!/bin/bash
# Script de Instalação/Reinstalação Automatizada - ULX Notebook Monitor (Versão Estável)

echo "===================================================="
echo "   ULX AUTOMATED INSTALLER & REINSTALLER            "
echo "===================================================="

# Pegar o caminho absoluto de onde o script está sendo executado
BASE_DIR=$(cd "$(dirname "$0")/../.." && pwd)

# 1. Desinstalação prévia (Limpeza)
echo "[1/3] Removendo versões anteriores..."
sudo rm -f /usr/local/bin/ulx-notebook-monitor 2>/dev/null
rm -f ./monitor 2>/dev/null
rm -f ./monitor.c 2>/dev/null

# 2. Instalação do Motor de Compilação
echo "[2/3] Configurando motor de compilação CLX..."
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
echo "[3/3] Compilando aplicativo nativamente (Modo Estável)..."
ulxc monitor.ulx

# 4. Entrega e Execução
if [ -f "./monitor" ]; then
    echo "----------------------------------------------------"
    echo "   INSTALAÇÃO CONCLUÍDA COM SUCESSO!                "
    echo "   Comando para usar: ulx-notebook-monitor          "
    echo "----------------------------------------------------"
    sudo cp ./monitor /usr/local/bin/ulx-notebook-monitor
    ulx-notebook-monitor
else
    echo "Erro fatal na compilação. O binário não foi gerado."
    exit 1
fi
