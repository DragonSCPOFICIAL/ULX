#!/bin/bash

# =============================================================================
# ULX UNINSTALLER - Remoção Completa e Limpa
# =============================================================================

echo "🗑️ Removendo o Ecossistema ULX do seu sistema..."

# 1. Remover binários e bibliotecas
sudo rm -rf /opt/ulx
sudo rm -f /usr/local/bin/ulx

# 2. Limpar variáveis de ambiente (remove a linha do .bashrc)
sed -i '/export ULX_PATH=\/opt\/ulx/d' ~/.bashrc

echo "✅ ULX foi removido com sucesso."
