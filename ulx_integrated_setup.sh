#!/bin/bash

# ULX INTEGRATED SETUP - SISTEMA DE PERFORMANCE DE METAL (Arch Linux)
# Este script integra o ULX Interceptor com a Linguagem de Programação ULX.

echo "========================================================="
echo "   ULX - SISTEMA DE PERFORMANCE DE METAL (v2.1.0)"
echo "========================================================="

# 1. Configurar o Compilador ULX para Performance
echo "[ULX] Configurando pipeline de compilação 'Metal'..."
# Ativar otimizações de AVX e Syscalls diretas no compilador Python
export ULX_OPTIMIZE_AVX=1
export ULX_USE_DIRECT_SYSCALLS=1

# 2. Compilar o Interceptor de Baixo Nível
echo "[INTERCEPTOR] Compilando ULX-Core e ULX-Vulkan..."
cd ulx-interceptor
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
cd ../..

# 3. Integrar com a Linguagem ULX
echo "[INTEGRATION] Vinculando a linguagem ULX ao Interceptor..."
# Copiar as bibliotecas compartilhadas para o diretório de runtime da linguagem
sudo mkdir -p /usr/local/lib/ulx/runtime
sudo cp ulx-interceptor/build/libulx_core.so /usr/local/lib/ulx/runtime/
sudo cp ulx-interceptor/build/libulx_vulkan.so /usr/local/lib/ulx/runtime/
sudo cp ulx-interceptor/gpu/ulx_vulkan_layer.json /usr/local/lib/ulx/runtime/

# 4. Criar o Wrapper de Execução 'ulx-run'
echo "[BIN] Criando utilitário 'ulx-run' para execução otimizada..."
cat <<EOF | sudo tee /usr/local/bin/ulx-run > /dev/null
#!/bin/bash
# ULX-RUN: Executa binários ULX com interceptação e otimização total.
export LD_PRELOAD="/usr/local/lib/ulx/runtime/libulx_core.so"
export VK_LAYER_PATH="/usr/local/lib/ulx/runtime/"
export VK_INSTANCE_LAYERS="VK_LAYER_ULX_OPTIMIZER"
export ULX_GPU_ENABLED=1
exec "\$@"
EOF
sudo chmod +x /usr/local/bin/ulx-run

echo "========================================================="
echo "INTEGRAÇÃO CONCLUÍDA: O ULX agora é uma linguagem de METAL."
echo "1. Compile seu código: ulxc seu_programa.ulx -o programa"
echo "2. Rode com performance total: ulx-run ./programa"
echo "========================================================="
