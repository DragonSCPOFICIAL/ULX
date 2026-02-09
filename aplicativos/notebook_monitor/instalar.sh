#!/bin/bash
# Script de Instalação/Reinstalação Automatizada - ULX Notebook Monitor

echo "===================================================="
echo "   ULX AUTOMATED INSTALLER & REINSTALLER            "
echo "===================================================="

# 1. Desinstalação prévia (Limpeza)
echo "[1/4] Removendo versões anteriores..."
sudo rm -f /usr/local/bin/ulx-notebook-monitor 2>/dev/null
rm -f ./monitor 2>/dev/null
rm -f ./monitor.c 2>/dev/null

# 2. Instalação de dependências e Ferramentas ULX
echo "[2/4] Configurando compilador CLX e ambiente LNX..."
# Garante que o ulxc global esteja atualizado
sudo cp ../../src/compiler/clx_compiler_intelligent.py /usr/local/bin/clx_engine.py 2>/dev/null
cat << 'EOF' > /tmp/ulxc
#!/bin/bash
python3 /usr/local/bin/clx_engine.py "$1"
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
    echo "Erro na compilação. Verifique o código ULX."
    exit 1
fi
