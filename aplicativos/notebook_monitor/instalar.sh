#!/bin/bash
# Script de Instalação/Reinstalação Automatizada - ULX Notebook Monitor

echo "===================================================="
echo "   ULX AUTOMATED INSTALLER & REINSTALLER            "
echo "===================================================="

# Pegar o caminho absoluto de onde o script está sendo executado
BASE_DIR=$(cd "$(dirname "$0")/../.." && pwd)

# 0. Instalação de dependências do sistema (Focado em Arch Linux)
if [ -f /etc/arch-release ]; then
    echo "[0/4] Detectado Arch Linux. Verificando dependências..."
    sudo pacman -Sy --needed --noconfirm gcc libgomp base-devel
else
    echo "[0/4] Verificando dependências básicas..."
fi

# 1. Desinstalação prévia (Limpeza)
echo "[1/4] Removendo versões anteriores e limpando ambiente..."
sudo rm -f /usr/local/bin/ulx-notebook-monitor 2>/dev/null
rm -f ./monitor 2>/dev/null
rm -f ./monitor.c 2>/dev/null

# 2. Instalação de dependências e Ferramentas ULX
echo "[2/4] Configurando compilador CLX e ambiente LNX..."
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

# 3. Compilação Nativa
echo "[3/4] Compilando aplicativo nativamente via CLX..."
ulxc monitor.ulx

# 4. Entrega e Execução
if [ -f "./monitor" ]; then
    echo "[4/4] Instalando binário no sistema..."
    sudo cp ./monitor /usr/local/bin/ulx-notebook-monitor
    echo "===================================================="
    echo "   INSTALAÇÃO CONCLUÍDA COM SUCESSO!                "
    echo "   Comando para usar: ulx-notebook-monitor          "
    echo "===================================================="
    ulx-notebook-monitor
else
    echo "Erro na compilação. Tentando modo de compatibilidade sem OpenMP..."
    # Fallback caso o erro de -lgomp persista
    sed -i 's/-fopenmp//g' /usr/local/bin/clx_engine.py 2>/dev/null
    ulxc monitor.ulx
    if [ -f "./monitor" ]; then
        sudo cp ./monitor /usr/local/bin/ulx-notebook-monitor
        ulx-notebook-monitor
    else
        echo "Falha crítica na compilação."
        exit 1
    fi
fi
