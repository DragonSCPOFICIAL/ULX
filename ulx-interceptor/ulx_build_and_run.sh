#!/bin/bash

# ULX BUILD & RUN - SISTEMA DE ENGENHARIA DE PERFORMANCE (Arch Linux)
# Este script gerencia a compilação e execução da camada de tradução ULX.

echo "========================================================="
echo "   ULX - SISTEMA DE ENGENHARIA DE PERFORMANCE (v1.0.0)"
echo "========================================================="

# 1. Verificar dependências (Arch Linux)
echo "[DEP] Verificando pacotes requeridos..."
for pkg in cmake gcc vulkan-devel mesa lib32-mesa; do
    if ! pacman -Qs $pkg > /dev/null; then
        echo "Aviso: Pacote $pkg não encontrado. Instale com 'sudo pacman -S $pkg'"
    fi
done

# 2. Compilação via CMake (Otimizada para Sandy Bridge)
echo "[BUILD] Iniciando compilação do ULX-Core e ULX-Vulkan..."
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

if [ $? -eq 0 ]; then
    echo "[BUILD] Compilação finalizada com sucesso."
else
    echo "[ERROR] Falha na compilação. Verifique os logs acima."
    exit 1
fi

# 3. Configuração do Ambiente de Execução
echo "[ENV] Configurando ambiente de interceptação..."
export LD_PRELOAD="./libulx_core.so"
export VK_LAYER_PATH="../gpu/"
export VK_INSTANCE_LAYERS="VK_LAYER_ULX_OPTIMIZER"
export ULX_GPU_ENABLED=1

# Otimizações de Driver Mesa/Intel
export INTEL_DEBUG=nocsum
export MESA_GLSL_CACHE_DISABLE=false
export MESA_SHADER_CACHE_DIR="./ulx_shader_cache"
mkdir -p $MESA_SHADER_CACHE_DIR

echo "========================================================="
echo "ULX ATIVADO: Otimização de CPU e GPU em tempo real."
echo "Para executar um jogo: ./ulx_build_and_run.sh <comando_do_jogo>"
echo "========================================================="

# Executar comando se fornecido
if [ ! -z "$1" ]; then
    exec "$@"
fi
