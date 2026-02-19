# ULX - Universal Linux eXecution (Performance de Metal)

O **ULX** é uma plataforma de desenvolvimento de performance extrema para **Arch Linux**, que integra uma linguagem de programação nativa com um interceptador de hardware de baixo nível para extrair o máximo de desempenho da CPU (AVX) e GPU (Vulkan).

**NOVIDADE: Agora com suporte nativo para arquivos .EXE e .APK sem emuladores visíveis, com instalação e configuração 100% automatizadas.**

---

## 🚀 Instalação Completa (Copia e Cola - UM ÚNICO BLOCO)

Este comando irá: **remover versões antigas**, clonar o repositório mais recente, instalar todas as dependências (incluindo o AUR helper `yay` se necessário), compilar o sistema e configurar a Ponte Universal (.exe/.apk). **Reinicie o sistema após a instalação.**

```bash
# --- SUPER BLOCO DE INSTALAÇÃO ULX ---
(
  REPO_URL="https://github.com/DragonSCPOFICIAL/ULX.git"
  INSTALL_DIR="${HOME}/ULX"
  
  echo -e "\033[0;32m[ULX]\033[0m Iniciando automação total no Arch Linux..."
  
  # Limpeza prévia para garantir atualização
  if [ -d "$INSTALL_DIR" ]; then
    echo -e "\033[0;33m[ULX]\033[0m Removendo versão antiga para atualização limpa..."
    sudo rm -rf "$INSTALL_DIR"
  fi
  
  # Clonagem e entrada no diretório
  echo -e "\033[0;32m[ULX]\033[0m Clonando repositório oficial..."
  git clone "$REPO_URL" "$INSTALL_DIR" || { echo -e "\033[0;31m[ERRO]\033[0m Falha ao clonar o repositório."; exit 1; }
  cd "$INSTALL_DIR"
  
  # Permissões e Execução
  chmod +x install.sh ulx_integrated_setup.sh ulx_universal_bridge.sh
  
  echo -e "\033[0;32m[ULX]\033[0m Executando instalador mestre (pode solicitar sua senha sudo)..."
  if sudo ./install.sh install; then
    echo -e "\n\033[0;32m=========================================================\033[0m"
    echo -e "\033[0;32m   ULX INSTALADO COM SUCESSO! REINICIE O SEU ARCH LINUX. \033[0m"
    echo -e "\033[0;32m=========================================================\033[0m"
  else
    echo -e "\n\033[0;31m[ERRO]\033[0m A instalação falhou. Verifique as mensagens acima."
    echo -e "\033[0;31m[DICA]\033[0m O terminal permanecerá aberto para você analisar o erro.\033[0m"
  fi
)
# --- FIM DO BLOCO ---
```

---

## 🗑️ Desinstalação Total (Copia e Cola - UM ÚNICO BLOCO)

Este comando irá: remover todas as configurações do sistema, desinstalar os drivers de tradução e **deletar permanentemente a pasta do repositório**.

```bash
# --- SUPER BLOCO DE DESINSTALAÇÃO ULX ---
(
  INSTALL_DIR="${HOME}/ULX"
  if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR"
    echo -e "\033[0;33m[ULX]\033[0m Iniciando remoção completa do sistema..."
    sudo ./install.sh uninstall
    cd "$HOME"
    sudo rm -rf "$INSTALL_DIR"
    echo -e "\n\033[0;32m[SUCESSO]\033[0m ULX e todos os seus arquivos foram removidos.\033[0m"
  else
    echo -e "\033[0;31m[AVISO]\033[0m Pasta do ULX não encontrada em $INSTALL_DIR.\033[0m"
  fi
)
# --- FIM DO BLOCO ---
```

---

## 🛠️ Como Funciona o "Metal"

Após reiniciar, o seu Arch Linux se torna universal:

1. **Execução Direta**: Clique duplo ou `./jogo.exe` / `./app.apk` no terminal. O ULX intercepta a chamada e usa a camada de tradução de baixo nível (Box64/Wine/Anbox) sem abrir emuladores.
2. **Performance**: O interceptador detecta seu **i7-2760QM** e força o uso de instruções **AVX** e **Vulkan**, aliviando a CPU e acelerando a GPU.
3. **Linguagem ULX**: Use `ulxc` para compilar códigos que conversam direto com o hardware.

*Desenvolvido para entusiastas de Arch Linux que buscam o máximo de controle e velocidade.*
