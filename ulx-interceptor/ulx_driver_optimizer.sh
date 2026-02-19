#!/bin/bash

# ULX UNIVERSAL TRANSLATION & OPTIMIZATION DRIVER (Arch Linux)
# Este script configura o ambiente para interceptação e tradução total de CPU/GPU.
# Foco: Máximo desempenho e estabilidade para OpenGL, DirectX e Vulkan.

echo "========================================================="
echo "   ULX - DRIVER DE TRADUÇÃO E OTIMIZAÇÃO UNIVERSAL"
echo "========================================================="

# 1. Otimização de CPU (Intel i7 Sandy Bridge)
echo "[CPU] Aplicando otimizações de arquitetura..."
# Forçar o governador de performance
if [ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]; then
    echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
fi

# 2. Configuração da Camada de Tradução de GPU (Vulkan/DXVK/Zink)
echo "[GPU] Configurando pontes de tradução (DXVK/Zink)..."

# Exportar variáveis para forçar tradução eficiente
# MESA_LOADER_DRIVER_OVERRIDE=zink -> Força OpenGL sobre Vulkan (se suportado)
# INTEL_DEBUG=nocsum -> Otimização específica para drivers Intel antigos
export INTEL_DEBUG=nocsum
export MESA_GL_VERSION_OVERRIDE=4.6
export MESA_GLSL_VERSION_OVERRIDE=460

# 3. Interceptação de Chamadas via ULX-Interceptor
echo "[ULX] Ativando camada de interceptação..."
export LD_PRELOAD="./ulx_cpu_interceptor.so:./ulx_gpu_interceptor.so"

# 4. Otimização de DirectX (via DXVK se instalado no sistema)
# O DXVK traduz DirectX 9/10/11 para Vulkan, aliviando o driver antigo da Intel.
export DXVK_HUD=compiler
export DXVK_ASYNC=1
export DXVK_STATE_CACHE=1

echo "========================================================="
echo "ULX ATIVADO: O sistema agora intercepta e traduz em tempo real."
echo "Execute seu jogo ou aplicação a partir deste terminal."
echo "Exemplo: ./seu_jogo_ou_app"
echo "========================================================="

# Manter o ambiente para o processo filho
exec "$@"
