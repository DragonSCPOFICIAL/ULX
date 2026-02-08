#!/bin/bash

# =============================================================================
# ULX UNINSTALLER - Remocao Completa e Limpa
# =============================================================================

echo "Removendo o Ecossistema ULX do seu sistema..."

# 1. Remover binarios e bibliotecas
sudo rm -rf /opt/ulx
sudo rm -f /usr/local/bin/ulx

# 2. Limpar variaveis de ambiente
sed -i '/export ULX_PATH=\/opt\/ulx/d' ~/.bashrc

echo "ULX foi removido com sucesso."
