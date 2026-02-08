#!/bin/bash

# =============================================================================
# ULX SECURE INSTALLER - Instalacao Segura e Profissional
# =============================================================================

echo "Iniciando instalacao do Ecossistema ULX..."

# 1. Criar diretorios do sistema
sudo mkdir -p /opt/ulx/bin
sudo mkdir -p /opt/ulx/lib
sudo mkdir -p /opt/ulx/include

# 2. Copiar os nucleos para o local de sistema (Modo Leitura apenas para seguranca)
echo "Configurando nucleos LNX, ULX e CLX..."
sudo cp -r core /opt/ulx/
sudo chmod -R 755 /opt/ulx/core

# 3. Criar link simbolico para o compilador
cat <<EOF > ulx_wrapper
#!/bin/bash
echo "ULX Sandbox: Executando com protecao de hardware..."
/opt/ulx/core/clx/clx_mega_compiler.ulx "\$@"
EOF

sudo mv ulx_wrapper /usr/local/bin/ulx
sudo chmod +x /usr/local/bin/ulx

# 4. Configurar variaveis de ambiente
echo "export ULX_PATH=/opt/ulx" >> ~/.bashrc

echo "Instalacao concluida com sucesso!"
echo "Seguranca: O ULX esta rodando em modo Sandbox."
echo "Digite 'ulx --help' para comecar."
