# ULX - Universal Linux eXecution (Performance de Metal)

O **ULX** é uma plataforma de desenvolvimento de performance extrema para **Arch Linux**, que integra uma linguagem de programação nativa com um interceptador de hardware de baixo nível para extrair o máximo de desempenho da CPU (AVX) e GPU (Vulkan).

**NOVIDADE: Agora com suporte nativo para arquivos .EXE e .APK sem emuladores visíveis, com instalação e configuração 100% automatizadas.**

---

## 🚀 Instalação Completa (Copia e Cola - Tudo Automático)

**PRÉ-REQUISITO:** Certifique-se de ter clonado o repositório ULX e navegado para o seu diretório.
Exemplo:
```bash
git clone https://github.com/DragonSCPOFICIAL/ULX.git
cd ULX
```

Após estar no diretório **ULX**, copie e cole **TODO** o bloco abaixo no seu terminal. Ele instalará todas as dependências, compilará o ULX e o Interceptor de Hardware, e configurará o sistema para executar `.exe` e `.apk` nativamente, sem nenhuma intervenção manual. **Reinicie o sistema após a instalação para que todas as alterações tenham efeito.**

```bash
# --- INÍCIO DO BLOCO DE INSTALAÇÃO ULX UNIVERSAL ---

# Sair imediatamente se um comando falhar
set -e

# Dar permissão de execução aos scripts
chmod +x install.sh ulx_integrated_setup.sh ulx_universal_bridge.sh || { echo "ERRO: Falha ao definir permissões de execução para os scripts."; exit 1; }

# Executar o script de instalação principal
sudo ./install.sh install || { echo "ERRO: A instalação do ULX falhou. Verifique as mensagens acima para detalhes."; exit 1; }

echo "\n========================================================="
echo "ULX UNIVERSAL INSTALADO COM SUCESSO! REINICIE O SISTEMA." 
echo "========================================================="

# --- FIM DO BLOCO DE INSTALAÇÃO ULX UNIVERSAL ---
```

---

## 🗑️ Desinstalação Completa (Copia e Cola - Tudo Automático)

**PRÉ-REQUISITO:** Certifique-se de estar no diretório raiz do repositório ULX.
Exemplo:
```bash
cd ULX
```

Após estar no diretório **ULX**, copie e cole **TODO** o bloco abaixo no seu terminal para remover completamente o ULX, a Ponte Universal e todos os arquivos relacionados do seu sistema, revertendo todas as configurações. **Reinicie o sistema após a desinstalação.**

```bash
# --- INÍCIO DO BLOCO DE DESINSTALAÇÃO ULX UNIVERSAL ---

# Sair imediatamente se um comando falhar
set -e

# Dar permissão de execução ao script de desinstalação
chmod +x install.sh || { echo "ERRO: Falha ao definir permissões de execução para o script de desinstalação."; exit 1; }

# Executar o script de desinstalação principal
sudo ./install.sh uninstall || { echo "ERRO: A desinstalação do ULX falhou. Verifique as mensagens acima para detalhes."; exit 1; }

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
