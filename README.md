# ULX - Universal Linux eXecution (Performance de Metal)

O **ULX** é uma plataforma de desenvolvimento de performance extrema para **Arch Linux**, que integra uma linguagem de programação nativa com um interceptador de hardware de baixo nível para extrair o máximo de desempenho da CPU (AVX) e GPU (Vulkan).

**NOVIDADE: Agora com suporte nativo para arquivos .EXE e .APK sem emuladores visíveis.**

---

## 🚀 Instalação Completa (Copia e Cola)

Copie e cole o bloco abaixo no seu terminal para instalar o compilador ULX, o Interceptor de Hardware, o suporte nativo para **.EXE** e **.APK** e configurar todo o ambiente automaticamente:

```bash
# Instalar dependências, compilar o ULX e ativar a Ponte Universal
sudo pacman -S --needed cmake gcc vulkan-devel mesa lib32-mesa nasm python wine-staging box64-git && \
chmod +x install.sh ulx_integrated_setup.sh ulx_universal_bridge.sh && \
./install.sh install && \
./ulx_integrated_setup.sh && \
sudo ./ulx_universal_bridge.sh && \
echo "ULX UNIVERSAL INSTALADO COM SUCESSO!"
```

---

## 🗑️ Desinstalação Completa (Copia e Cola)

Copie e cole o bloco abaixo no seu terminal para remover completamente o ULX, a Ponte Universal e todos os arquivos relacionados do seu sistema:

```bash
# Remover binários, bibliotecas e desativar binfmt_misc
sudo rm -f /usr/local/bin/ulxc /usr/local/bin/ulx-run /usr/local/bin/ulx-run-exe /usr/local/bin/ulx-run-apk && \
sudo rm -rf /usr/local/lib/ulx /usr/local/share/ulx && \
[ -f /proc/sys/fs/binfmt_misc/ulx-exe ] && echo -1 | sudo tee /proc/sys/fs/binfmt_misc/ulx-exe && \
[ -f /proc/sys/fs/binfmt_misc/ulx-apk ] && echo -1 | sudo tee /proc/sys/fs/binfmt_misc/ulx-apk && \
make clean && \
echo "ULX REMOVIDO COMPLETAMENTE!"
```

---

## 🛠️ Como Usar

1. **Compilar seu código ULX**:
   ```bash
   ulxc seu_programa.ulx -o meu_app
   ```

2. **Executar Jogos/Apps Windows (.exe) ou Android (.apk)**:
   *Basta dar permissão de execução e rodar diretamente:*
   ```bash
   chmod +x jogo.exe
   ./jogo.exe
   ```

3. **Executar com Performance de Metal (AVX/Vulkan)**:
   ```bash
   ulx-run ./meu_app
   ```

*Nota: O ULX utiliza syscalls diretas do Linux e otimizações de hardware nativas para garantir que seu código seja o mais rápido possível, independentemente do formato original.*
