# ULX - Universal Linux eXecution (Performance de Metal)

O **ULX** é uma plataforma de desenvolvimento de performance extrema para **Arch Linux**, que integra uma linguagem de programação nativa com um interceptador de hardware de baixo nível para extrair o máximo de desempenho da CPU (AVX) e GPU (Vulkan).

**NOVIDADE: Agora com suporte nativo para arquivos .EXE e .APK sem emuladores visíveis, com instalação e configuração 100% automatizadas.**

---

## 🚀 Instalação Completa (Copia e Cola - Tudo Automático)

Copie e cole **TODO** o bloco abaixo no seu terminal. Ele instalará todas as dependências, compilará o ULX e o Interceptor de Hardware, e configurará o sistema para executar `.exe` e `.apk` nativamente, sem nenhuma intervenção manual. **Reinicie o sistema após a instalação para que todas as alterações tenham efeito.**

```bash
# --- INÍCIO DO BLOCO DE INSTALAÇÃO ULX UNIVERSAL ---

# 1. Instalar dependências essenciais via pacman
sudo pacman -Syu --needed --noconfirm cmake gcc vulkan-devel mesa lib32-mesa nasm python wine-staging git base-devel || { echo "Erro: Falha ao instalar dependências via pacman."; exit 1; }

# 2. Verificar e instalar AUR helper (yay ou paru) ou instruir instalação manual
if command -v yay &> /dev/null; then
    AUR_HELPER="yay"
elif command -v paru &> /dev/null; then
    AUR_HELPER="paru"
else
    echo "
AVISO: Nenhum AUR helper (yay ou paru) encontrado.
Para instalar box64-git e anbox-git, você precisará de um AUR helper.
Por favor, instale 'yay' ou 'paru' manualmente ou instale os pacotes do AUR manualmente.
Exemplo para yay:
  git clone https://aur.archlinux.org/yay.git
  cd yay
  makepkg -si
  cd ..
  rm -rf yay
Reinicie este script após instalar o AUR helper.
"
    exit 1
fi

# 3. Instalar pacotes do AUR (box64-git e anbox-git) via AUR helper
${AUR_HELPER} -S --noconfirm box64-git anbox-git || { echo "Erro: Falha ao instalar pacotes do AUR (${AUR_HELPER})."; exit 1; }

# 4. Executar scripts de instalação e configuração do ULX
chmod +x install.sh ulx_integrated_setup.sh ulx_universal_bridge.sh || { echo "Erro: Falha ao definir permissões de execução."; exit 1; }
sudo ./install.sh install || { echo "Erro: Falha na instalação principal do ULX."; exit 1; }

echo "\n========================================================="
echo "ULX UNIVERSAL INSTALADO COM SUCESSO! REINICIE O SISTEMA." 
echo "========================================================="

# --- FIM DO BLOCO DE INSTALAÇÃO ULX UNIVERSAL ---
```

---

## 🗑️ Desinstalação Completa (Copia e Cola - Tudo Automático)

Copie e cole **TODO** o bloco abaixo no seu terminal para remover completamente o ULX, a Ponte Universal e todos os arquivos relacionados do seu sistema, revertendo todas as configurações. **Reinicie o sistema após a desinstalação.**

```bash
# --- INÍCIO DO BLOCO DE DESINSTALAÇÃO ULX UNIVERSAL ---

# 1. Remover pacotes do AUR (box64-git e anbox-git) via AUR helper
if command -v yay &> /dev/null; then
    AUR_HELPER="yay"
elif command -v paru &> /dev/null; then
    AUR_HELPER="paru"
else
    echo "AVISO: Nenhum AUR helper (yay ou paru) encontrado. Remova 'box64-git' e 'anbox-git' manualmente se os instalou via AUR."
fi

if [ -n "${AUR_HELPER}" ]; then
    ${AUR_HELPER} -R --noconfirm box64-git anbox-git || echo "Aviso: Falha ao remover pacotes do AUR (${AUR_HELPER}). Pode ser que já não estejam instalados."
fi

# 2. Executar script de desinstalação do ULX
sudo ./install.sh uninstall || { echo "Erro: Falha na desinstalação principal do ULX."; exit 1; }

# 3. Limpar dependências principais (opcional, remova apenas se não precisar mais)
# sudo pacman -Rns --noconfirm cmake gcc vulkan-devel mesa lib32-mesa nasm python wine-staging git base-devel || echo "Aviso: Falha ao remover dependências via pacman. Pode ser que já não estejam instaladas ou sejam usadas por outros programas."

echo "\n========================================================="
echo "ULX REMOVIDO COMPLETAMENTE! REINICIE O SISTEMA." 
echo "========================================================="

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
