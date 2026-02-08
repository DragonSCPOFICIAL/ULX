#!/bin/bash

# ULX-Integrator: Registra o formato .ulx como um tipo nativo no Linux
# Mantenedor: DragonSCPOFICIAL & Manus

MIME_DIR="/usr/share/mime/packages"
ICON_DIR="/usr/share/icons/hicolor/48x48/apps"
APP_DIR="/usr/share/applications"

echo "[ULX] Iniciando integração de sistema..."

# 1. Criar o arquivo de definição MIME
cat <<EOF | sudo tee $MIME_DIR/ulx-package.xml > /dev/null
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="application/x-ulx">
        <comment>Aplicativo Universal ULX</comment>
        <glob pattern="*.ulx"/>
        <icon name="ulx-package"/>
    </mime-type>
</mime-info>
EOF

# 2. Atualizar o banco de dados MIME
sudo update-mime-database /usr/share/mime

# 3. Criar um script 'handler' inteligente para arquivos .ulx
cat <<EOF | sudo tee /usr/bin/ulx-handler > /dev/null
#!/bin/bash
# O Handler agora usa o ULX-Player para execução nativa instantânea
# Se estiver no terminal, apenas roda. Se for via GUI, também roda direto.
ulx-run "\$1"
EOF
sudo chmod +x /usr/bin/ulx-handler

# 4. Criar a associação de desktop para o handler
cat <<EOF | sudo tee $APP_DIR/ulx-handler.desktop > /dev/null
[Desktop Entry]
Type=Application
Name=ULX Package Handler
Exec=ulx-handler %f
MimeType=application/x-ulx;
NoDisplay=true
EOF

echo "[ULX] Integração concluída! O sistema agora reconhece arquivos .ulx."
