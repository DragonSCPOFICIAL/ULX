# ULX - Universal Linux eXecution (Performance de Metal)

O **ULX** é uma plataforma de desenvolvimento de performance extrema para **Arch Linux**, que integra uma linguagem de programação nativa com um interceptador de hardware de baixo nível para extrair o máximo de desempenho da CPU (AVX) e GPU (Vulkan).

**NOVIDADE: Agora com suporte nativo para arquivos .EXE e .APK sem emuladores visíveis, com instalação e configuração 100% automatizadas.**

---

## 🚀 Instalação Completa (Copia e Cola - Tudo Automático)

Copie e cole **TODO** o bloco abaixo no seu terminal. Ele instalará todas as dependências, compilará o ULX e o Interceptor de Hardware, e configurará o sistema para executar `.exe` e `.apk` nativamente, sem nenhuma intervenção manual. **Reinicie o sistema após a instalação para que todas as alterações tenham efeito.**

```bash
# Instalar dependências, compilar o ULX e ativar a Ponte Universal
sudo pacman -Syu --needed --noconfirm cmake gcc vulkan-devel mesa lib32-mesa nasm python wine-staging box64-git anbox-git && \
chmod +x install.sh ulx_integrated_setup.sh ulx_universal_bridge.sh && \
sudo ./install.sh install && \
echo "\n=========================================================" && \
echo "ULX UNIVERSAL INSTALADO COM SUCESSO! REINICIE O SISTEMA." && \
echo "========================================================="
```

---

## 🗑️ Desinstalação Completa (Copia e Cola - Tudo Automático)

Copie e cole **TODO** o bloco abaixo no seu terminal para remover completamente o ULX, a Ponte Universal e todos os arquivos relacionados do seu sistema, revertendo todas as configurações. **Reinicie o sistema após a desinstalação.**

```bash
# Remover binários, bibliotecas, configurações de binfmt e MIME types
sudo ./install.sh uninstall && \
echo "\n=========================================================" && \
echo "ULX REMOVIDO COMPLETAMENTE! REINICIE O SISTEMA." && \
echo "========================================================="
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
