#!/bin/bash

# ULX System Monitor - Instalador
# Transforma o executável em um programa de sistema instalado

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          ULX System Monitor - Instalador                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se é root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[✗] Este script precisa ser executado como root!${NC}"
   echo ""
   echo "Use: sudo bash install.sh"
   exit 1
fi

echo -e "${YELLOW}[*] Iniciando instalação...${NC}"
echo ""

# 1. Copiar binário para /usr/local/bin/
echo -e "${YELLOW}[1/5] Copiando binário para /usr/local/bin/...${NC}"
if [ -f "system-monitor" ]; then
    cp system-monitor /usr/local/bin/ulx-monitor
    chmod +x /usr/local/bin/ulx-monitor
    echo -e "${GREEN}[✓] Binário instalado em /usr/local/bin/ulx-monitor${NC}"
else
    echo -e "${RED}[✗] Arquivo 'system-monitor' não encontrado!${NC}"
    exit 1
fi
echo ""

# 2. Criar arquivo .desktop para menu de aplicativos
echo -e "${YELLOW}[2/5] Criando atalho no menu de aplicativos...${NC}"
mkdir -p /usr/share/applications
cat > /usr/share/applications/ulx-monitor.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=ULX System Monitor
Comment=Monitor de Sistema em Tempo Real
Exec=ulx-monitor
Icon=utilities-system-monitor
Categories=System;Utility;
Terminal=true
EOF
chmod 644 /usr/share/applications/ulx-monitor.desktop
echo -e "${GREEN}[✓] Atalho criado em /usr/share/applications/ulx-monitor.desktop${NC}"
echo ""

# 3. Criar arquivo de man page (documentação)
echo -e "${YELLOW}[3/5] Criando documentação (man page)...${NC}"
mkdir -p /usr/share/man/man1
cat > /usr/share/man/man1/ulx-monitor.1 << 'EOF'
.TH ULX-MONITOR 1 "Fevereiro 2026" "ULX 1.0" "Utilitários do Sistema"
.SH NOME
ulx-monitor \- Monitor de Sistema em Tempo Real
.SH SINOPSE
.B ulx-monitor
.SH DESCRIÇÃO
Monitor de Sistema que mostra em tempo real:
.IP \(bu 2
CPU (cores, modelo, frequência)
.IP \(bu 2
Memória (total, usada, disponível)
.IP \(bu 2
Armazenamento (discos, uso)
.IP \(bu 2
Uptime (tempo ligado)
.IP \(bu 2
Top 5 Processos (maior uso de CPU/RAM)
.IP \(bu 2
Rede (interfaces ativas)
.SH EXEMPLOS
Executar o monitor:
.IP
ulx-monitor
.PP
Para sair, pressione Ctrl+C
.SH AUTOR
Dragon SCP Official
.SH VEJA TAMBÉM
top(1), htop(1), free(1)
EOF
chmod 644 /usr/share/man/man1/ulx-monitor.1
echo -e "${GREEN}[✓] Documentação criada em /usr/share/man/man1/ulx-monitor.1${NC}"
echo ""

# 4. Criar script de desinstalação
echo -e "${YELLOW}[4/5] Criando script de desinstalação...${NC}"
cat > /usr/local/bin/uninstall-ulx-monitor << 'EOF'
#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          ULX System Monitor - Desinstalador                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

if [[ $EUID -ne 0 ]]; then
   echo "[✗] Este script precisa ser executado como root!"
   echo "Use: sudo uninstall-ulx-monitor"
   exit 1
fi

echo "[*] Desinstalando ULX System Monitor..."
echo ""

# Remover binário
if [ -f "/usr/local/bin/ulx-monitor" ]; then
    rm -f /usr/local/bin/ulx-monitor
    echo "[✓] Binário removido"
fi

# Remover atalho
if [ -f "/usr/share/applications/ulx-monitor.desktop" ]; then
    rm -f /usr/share/applications/ulx-monitor.desktop
    echo "[✓] Atalho removido"
fi

# Remover man page
if [ -f "/usr/share/man/man1/ulx-monitor.1" ]; then
    rm -f /usr/share/man/man1/ulx-monitor.1
    echo "[✓] Documentação removida"
fi

# Remover script de desinstalação
rm -f /usr/local/bin/uninstall-ulx-monitor
echo "[✓] Script de desinstalação removido"

echo ""
echo "[✓] ULX System Monitor foi desinstalado com sucesso!"
EOF
chmod +x /usr/local/bin/uninstall-ulx-monitor
echo -e "${GREEN}[✓] Script de desinstalação criado${NC}"
echo ""

# 5. Atualizar banco de dados do man
echo -e "${YELLOW}[5/5] Atualizando banco de dados...${NC}"
mandb > /dev/null 2>&1 || true
echo -e "${GREEN}[✓] Banco de dados atualizado${NC}"
echo ""

# Resumo final
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   INSTALAÇÃO CONCLUÍDA!                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}[✓] ULX System Monitor foi instalado com sucesso!${NC}"
echo ""
echo "📍 Localização do binário: /usr/local/bin/ulx-monitor"
echo "📍 Atalho no menu: /usr/share/applications/ulx-monitor.desktop"
echo "📍 Documentação: man ulx-monitor"
echo ""
echo "🚀 Para executar:"
echo "   ulx-monitor"
echo ""
echo "❌ Para desinstalar:"
echo "   sudo uninstall-ulx-monitor"
echo ""
echo "📖 Para ler a documentação:"
echo "   man ulx-monitor"
echo ""
