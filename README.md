# ULX - Universal Linux eXecution (Performance de Metal)

O **ULX** é uma plataforma de desenvolvimento de performance extrema para **Arch Linux**, que integra uma linguagem de programação nativa com um interceptador de hardware de baixo nível para extrair o máximo de desempenho da CPU (AVX) e GPU (Vulkan).

---

## 🚀 Instalação Completa (Copia e Cola)

Copie e cole o bloco abaixo no seu terminal para instalar o compilador ULX, o Interceptor de Hardware e configurar todo o ambiente automaticamente:

```bash
# Instalar dependências, compilar o ULX e o Interceptor de Hardware
sudo pacman -S --needed cmake gcc vulkan-devel mesa lib32-mesa nasm python && \
chmod +x install.sh ulx_integrated_setup.sh && \
./install.sh install && \
./ulx_integrated_setup.sh && \
echo "ULX INSTALADO COM SUCESSO!"
```

---

## 🗑️ Desinstalação Completa (Copia e Cola)

Copie e cole o bloco abaixo no seu terminal para remover completamente o ULX, o Interceptor e todos os arquivos relacionados do seu sistema:

```bash
# Remover binários, bibliotecas e pastas do ULX
sudo rm -f /usr/local/bin/ulxc /usr/local/bin/ulx-run && \
sudo rm -rf /usr/local/lib/ulx /usr/local/share/ulx && \
make clean && \
echo "ULX REMOVIDO COMPLETAMENTE!"
```

---

## 🛠️ Como Usar

1. **Compilar seu código ULX**:
   ```bash
   ulxc seu_programa.ulx -o meu_app
   ```

2. **Executar com Performance de Metal (AVX/Vulkan)**:
   ```bash
   ulx-run ./meu_app
   ```

*Nota: O ULX utiliza syscalls diretas do Linux e otimizações de hardware nativas para garantir que seu código seja o mais rápido possível.*
