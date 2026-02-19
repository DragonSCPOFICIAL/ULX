cmake_minimum_required(VERSION 3.10)
project(ULX_Interceptor VERSION 1.0.0 LANGUAGES CXX)

# ULX Interceptor & Translation Layer (Arch Linux)
# Configuração de Compilação Profissional

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Otimizações para Sandy Bridge (i7-2760QM)
# -march=sandybridge ativa extensões AVX e SSE4.2 nativas
# -O3 ativa otimizações agressivas de performance
add_compile_options(-march=sandybridge -O3 -fPIC -Wall -Wextra)

# Bibliotecas Requeridas
find_package(Vulkan REQUIRED)
find_package(Threads REQUIRED)

# --- Alvo: ULX-Core (CPU Interceptor) ---
add_library(ulx_core SHARED cpu/ulx_core.cpp)
target_link_libraries(ulx_core PRIVATE dl Threads::Threads)
set_target_properties(ulx_core PROPERTIES OUTPUT_NAME "ulx_core")

# --- Alvo: ULX-Vulkan (GPU Interceptor Layer) ---
add_library(ulx_vulkan SHARED gpu/ulx_vulkan_layer.cpp)
target_include_directories(ulx_vulkan PRIVATE ${Vulkan_INCLUDE_DIRS})
target_link_libraries(ulx_vulkan PRIVATE ${Vulkan_LIBRARIES} dl)
set_target_properties(ulx_vulkan PROPERTIES OUTPUT_NAME "ulx_vulkan")

# --- Instalação ---
install(TARGETS ulx_core ulx_vulkan DESTINATION /usr/local/lib/ulx)
