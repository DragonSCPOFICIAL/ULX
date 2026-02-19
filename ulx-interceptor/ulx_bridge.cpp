#include <iostream>
#include <vulkan/vulkan.h>
#include <dlfcn.h>

/**
 * ULX-Bridge: Biblioteca de Runtime para a Linguagem ULX
 * Conecta o código compilado da linguagem ULX com o Interceptor e a GPU.
 */

extern "C" {

    /**
     * ulx_gpu_dispatch_submit: Despacha comandos de GPU da linguagem ULX
     * para a camada de interceptação Vulkan.
     */
    void ulx_gpu_dispatch_submit() {
        // No futuro: Receber o Command Buffer gerado pela linguagem ULX
        // e submetê-lo via Vulkan com otimizações.
        
        // std::cout << "[ULX-BRIDGE]: Despachando comando de GPU para o hardware...\n";
    }

    /**
     * ulx_init_hardware: Inicializa as extensões de hardware (AVX/Vulkan)
     * para o programa escrito em ULX.
     */
    void ulx_init_hardware() {
        // Verificar suporte a AVX
        unsigned int eax, ebx, ecx, edx;
        __get_cpuid(1, &eax, &ebx, &ecx, &edx);
        bool has_avx = (ecx & bit_AVX) != 0;

        if (has_avx) {
            // std::cout << "[ULX-BRIDGE]: Extensões AVX detectadas e ativadas.\n";
        }
    }
}

// Helper para CPUID
#include <cpuid.h>
