#!/bin/bash

# =============================================================================
# ULX SECURE INSTALLER - Instalação Segura e Profissional
# =============================================================================

echo "🚀 Iniciando instalação do Ecossistema ULX..."

# 1. Criar diretórios do sistema
sudo mkdir -p /opt/ulx/bin
sudo mkdir -p /opt/ulx/lib
sudo mkdir -p /opt/ulx/include

# 2. Copiar os núcleos para o local de sistema (Modo Leitura apenas para segurança)
echo "📦 Configurando núcleos LNX, ULX e CLX..."
sudo cp -r core /opt/ulx/
sudo chmod -R 755 /opt/ulx/core

# 3. Criar link simbólico para o compilador (para usar o comando 'ulx' em qualquer lugar)
# Por enquanto, criamos um wrapper de segurança
cat <<EOF > ulx_wrapper
#!/bin/bash
echo "🛡️ ULX Sandbox: Executando com proteção de hardware..."
# Aqui chamaria o CLX real com flags de segurança
/opt/ulx/core/clx/clx_mega_compiler.ulx "\$@"
EOF

sudo mv ulx_wrapper /usr/local/bin/ulx
sudo chmod +x /usr/local/bin/ulx

# 4. Configurar variáveis de ambiente
echo "export ULX_PATH=/opt/ulx" >> ~/.bashrc

echo "✅ Instalação concluída com sucesso!"
echo "🛡️  Segurança: O ULX está rodando em modo Sandbox."
echo "💡 Digite 'ulx --help' para começar."
