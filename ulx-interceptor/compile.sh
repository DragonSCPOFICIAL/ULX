#!/bin/bash

# ULX Interceptor - Script de Compilação (Arch Linux)
# Este script compila os interceptadores como bibliotecas compartilhadas (.so)

echo "--- ULX Interceptor Build ---"

# Compilar Interceptador de CPU
echo "Compilando CPU Interceptor..."
gcc -shared -fPIC -o ulx_cpu_interceptor.so cpu/ulx_cpu_interceptor.c -ldl
if [ $? -eq 0 ]; then
    echo "CPU Interceptor: OK (ulx_cpu_interceptor.so)"
else
    echo "Erro ao compilar CPU Interceptor"
fi

# Compilar Interceptador de GPU (Requer bibliotecas de desenvolvimento OpenGL)
echo "Compilando GPU Interceptor..."
gcc -shared -fPIC -o ulx_gpu_interceptor.so gpu/ulx_gpu_interceptor.c -ldl -lGL
if [ $? -eq 0 ]; then
    echo "GPU Interceptor: OK (ulx_gpu_interceptor.so)"
else
    echo "Erro ao compilar GPU Interceptor (Certifique-se de ter os headers OpenGL instalados)"
fi

echo "--- Build Finalizado ---"
echo "Para testar (CPU): LD_PRELOAD=./ulx_cpu_interceptor.so ls"
echo "Para testar (GPU): LD_PRELOAD=./ulx_gpu_interceptor.so <aplicacao_opengl>"
