# ULX - Universal Linux eXecution (Performance de Metal)

O **ULX** é uma plataforma de desenvolvimento de performance extrema para **Arch Linux**, que integra uma linguagem de programação nativa com um interceptador de hardware de baixo nível para extrair o máximo de desempenho da CPU (AVX) e GPU (Vulkan).

**NOVIDADE: Agora com suporte nativo para arquivos .EXE e .APK sem emuladores visíveis, com instalação e configuração 100% automatizadas.**

---

## 🚀 Instalação Completa (Copia e Cola - Tudo Automático)

Copie e cole **TODO** o bloco abaixo no seu terminal. Ele fará uma instalação limpa do ULX, incluindo a clonagem do repositório, instalação de todas as dependências (pacman e AUR), compilação do ULX e do Interceptor de Hardware, e configurará o sistema para executar `.exe` e `.apk` nativamente, sem nenhuma intervenção manual. **Reinicie o sistema após a instalação para que todas as alterações tenham efeito.**

```bash
# --- INÍCIO DO BLOCO DE INSTALAÇÃO ULX UNIVERSAL ---

# Sair imediatamente se um comando falhar, mas com tratamento de erro
set -e

# Definir diretório de instalação
INSTALL_DIR="${HOME}/ULX"
REPO_URL="https://github.com/DragonSCPOFICIAL/ULX.git"

# Função de tratamento de erro para o bloco
install_error_handler() {
    local last_exit_code=$?
    echo -e "\n\033[0;31m[ERRO CRÍTICO]\033[0m A instalação do ULX falhou na etapa anterior. Código de saída: ${last_exit_code}"
    echo -e "\033[0;31m[ERRO CRÍTICO]\033[0m Por favor, revise as mensagens acima para detalhes e tente novamente.\033[0m"
    exit 1
}
trap install_error_handler ERR

echo -e "\033[0;32m[INFO]\033[0m Iniciando instalação ULX Universal..."

# 1. Remover instalação anterior (se existir) e clonar o repositório
if [ -d "${INSTALL_DIR}" ]; then
    echo -e "\033[0;33m[AVISO]\033[0m Diretório ULX existente detectado. Removendo para uma instalação limpa..."
    sudo rm -rf "${INSTALL_DIR}"
fi

echo -e "\033[0;32m[INFO]\033[0m Clonando repositório ULX..."
git clone "${REPO_URL}" "${INSTALL_DIR}"

# 2. Navegar para o diretório do repositório
cd "${INSTALL_DIR}"

# 3. Dar permissão de execução aos scripts
echo -e "\033[0;32m[INFO]\033[0m Definindo permissões de execução para scripts..."
chmod +x install.sh ulx_integrated_setup.sh ulx_universal_bridge.sh

# 4. Executar o script de instalação principal
echo -e "\033[0;32m[INFO]\033[0m Executando script de instalação principal..."
sudo ./install.sh install

echo -e "\n========================================================="
echo -e "\033[0;32mULX UNIVERSAL INSTALADO COM SUCESSO! REINICIE O SISTEMA.\033[0m" 
echo -e "========================================================="

# --- FIM DO BLOCO DE INSTALAÇÃO ULX UNIVERSAL ---
```

---

## 🗑️ Desinstalação Completa (Copia e Cola - Tudo Automático)

Copie e cole **TODO** o bloco abaixo no seu terminal para remover completamente o ULX, a Ponte Universal e todos os arquivos relacionados do seu sistema, incluindo a pasta do repositório. **Reinicie o sistema após a desinstalação.**

```bash
# --- INÍCIO DO BLOCO DE DESINSTALAÇÃO ULX UNIVERSAL ---

# Sair imediatamente se um comando falhar, mas com tratamento de erro
set -e

# Definir diretório de instalação
INSTALL_DIR="${HOME}/ULX"

# Função de tratamento de erro para o bloco
uninstall_error_handler() {
    local last_exit_code=$?
    echo -e "\n\033[0;31m[ERRO CRÍTICO]\033[0m A desinstalação do ULX falhou na etapa anterior. Código de saída: ${last_exit_code}"
    echo -e "\033[0;31m[ERRO CRÍTICO]\033[0m Por favor, revise as mensagens acima para detalhes e tente novamente.\033[0m"
    exit 1
}
trap uninstall_error_handler ERR

echo -e "\033[0;32m[INFO]\033[0m Iniciando desinstalação ULX Universal..."

# 1. Navegar para o diretório do repositório (se existir)
if [ -d "${INSTALL_DIR}" ]; then
    cd "${INSTALL_DIR}"
    # 2. Executar o script de desinstalação principal
    echo -e "\033[0;32m[INFO]\033[0m Executando script de desinstalação principal..."
    sudo ./install.sh uninstall
    # 3. Remover o diretório do repositório
    echo -e "\033[0;32m[INFO]\033[0m Removendo diretório do repositório ULX..."
    cd "${HOME}"
    sudo rm -rf "${INSTALL_DIR}"
else
    echo -e "\033[0;33m[AVISO]\033[0m Diretório ULX não encontrado em ${INSTALL_DIR}. Pulando remoção de arquivos locais."
    # Ainda tentar limpar binfmt e mime types caso o diretório tenha sido removido manualmente
    echo -e "\033[0;32m[INFO]\033[0m Tentando limpar configurações residuais do sistema..."
    sudo rm -f /etc/binfmt.d/ulx-exe.conf /etc/binfmt.d/ulx-apk.conf
    [ -f /proc/sys/fs/binfmt_misc/ulx-exe ] && echo -1 | sudo tee /proc/sys/fs/binfmt_misc/ulx-exe > /dev/null
    [ -f /proc/sys/fs/binfmt_misc/ulx-apk ] && echo -1 | sudo tee /proc/sys/fs/binfmt_misc/ulx-apk > /dev/null
    sudo systemctl restart systemd-binfmt || echo -e "\033[0;33m[AVISO]\033[0m Falha ao reiniciar systemd-binfmt. Pode ser necessário reiniciar manualmente."
    sudo rm -f /usr/share/mime/packages/ulx-exe.xml /usr/share/mime/packages/ulx-apk.xml
    sudo update-mime-database /usr/share/mime || echo -e "\033[0;33m[AVISO]\033[0m Falha ao atualizar banco de dados MIME. Pode ser necessário reiniciar manualmente."
fi

echo -e "\n========================================================="
echo -e "\033[0;32mULX REMOVIDO COMPLETAMENTE! REINICIE O SISTEMA.\033[0m" 
echo -e "========================================================="

# --- FIM DO BLOCO DE DESINSTALAÇÃO ULX UNIVERSAL ---
```

---

## 🛠️ Como Usar

Após a instalação e reinício do sistema:

1. **Compilar seu código ULX**:
   ```bash
   ulxc seu_programa.ulx -o meu_app
   ```

2. **Executar Jogos/Apps Windows (.exe) ou Android (.apk)**:
   *Basta dar permissão de execução e rodar diretamente. O sistema operacional já saberá como abri-los:*
   ```bash
   chmod +x meu_jogo.exe
   ./meu_jogo.exe
   ```
   ou
   ```bash
   chmod +x meu_app.apk
   ./meu_app.apk
   ```

3. **Executar com Performance de Metal (AVX/Vulkan)**:
   ```bash
   ulx-run ./meu_app
   ```

*Nota: O ULX utiliza syscalls diretas do Linux e otimizações de hardware nativas para garantir que seu código seja o mais rápido possível, independentemente do formato original.*
