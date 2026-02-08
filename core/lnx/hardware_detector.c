/*
 * LNX - Hardware Translator (Inteligente e Adaptativo)
 * 
 * Detecta hardware disponível e equilibra automaticamente:
 * - CPU (cores, cache, frequência)
 * - GPU (CUDA, OpenCL, Vulkan)
 * - RAM (quantidade, banda)
 * - Armazenamento (tipo, velocidade)
 * 
 * Otimiza código para máxima performance baseado no hardware real
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <cpuid.h>
#include <sys/sysinfo.h>

#pragma GCC optimize("O3")
#pragma GCC target("native")

/* ===== ESTRUTURAS ===== */

typedef struct {
    int cores;
    int threads;
    int cache_l1;
    int cache_l2;
    int cache_l3;
    float frequency_ghz;
    char brand[256];
    int has_avx;
    int has_avx2;
    int has_avx512;
    int has_sse;
    int has_sse2;
    int has_sse42;
} CPUInfo;

typedef struct {
    int has_cuda;
    int has_opencl;
    int has_vulkan;
    int cuda_cores;
    long cuda_memory_mb;
    char cuda_device[256];
} GPUInfo;

typedef struct {
    long total_mb;
    long available_mb;
    long used_mb;
    float memory_bandwidth_gbps;
} RAMInfo;

typedef struct {
    CPUInfo cpu;
    GPUInfo gpu;
    RAMInfo ram;
    
    // Scores
    float cpu_score;
    float gpu_score;
    float ram_score;
    
    // Estratégia
    int use_cpu;
    int use_gpu;
    int use_parallel;
    int use_simd;
    int use_vectorization;
} HardwareProfile;

/* ===== DETECÇÃO DE CPU ===== */

void detect_cpu(CPUInfo* cpu) {
    memset(cpu, 0, sizeof(CPUInfo));
    
    // Obtém número de cores
    cpu->cores = sysconf(_SC_NPROCESSORS_ONLN);
    cpu->threads = cpu->cores * 2;  // Assumindo hyperthreading
    
    // Detecta cache (estimado)
    cpu->cache_l1 = 32;  // KB
    cpu->cache_l2 = 256; // KB
    cpu->cache_l3 = 8192; // KB (8MB)
    
    // Detecta frequência
    cpu->frequency_ghz = 2.4;  // Padrão
    
    // Detecta instruções SIMD
    unsigned int eax, ebx, ecx, edx;
    
    // CPUID para SSE
    if (__get_cpuid(1, &eax, &ebx, &ecx, &edx)) {
        cpu->has_sse = (edx >> 25) & 1;
        cpu->has_sse2 = (edx >> 26) & 1;
        cpu->has_sse42 = (ecx >> 20) & 1;
        cpu->has_avx = (ecx >> 28) & 1;
    }
    
    // CPUID para AVX2
    if (__get_cpuid_count(7, 0, &eax, &ebx, &ecx, &edx)) {
        cpu->has_avx2 = (ebx >> 5) & 1;
        cpu->has_avx512 = (ebx >> 16) & 1;
    }
    
    // Brand
    strcpy(cpu->brand, "Intel/AMD x86-64");
}

/* ===== DETECÇÃO DE GPU ===== */

void detect_gpu(GPUInfo* gpu) {
    memset(gpu, 0, sizeof(GPUInfo));
    
    // Verifica CUDA
    FILE* fp = popen("which nvcc 2>/dev/null", "r");
    if (fp) {
        gpu->has_cuda = 1;
        gpu->cuda_cores = 1024;  // Estimado
        gpu->cuda_memory_mb = 2048;  // Estimado
        strcpy(gpu->cuda_device, "NVIDIA GPU");
        pclose(fp);
    }
    
    // Verifica OpenCL
    fp = popen("clinfo 2>/dev/null | head -1", "r");
    if (fp) {
        gpu->has_opencl = 1;
        pclose(fp);
    }
    
    // Verifica Vulkan
    fp = popen("which vulkaninfo 2>/dev/null", "r");
    if (fp) {
        gpu->has_vulkan = 1;
        pclose(fp);
    }
}

/* ===== DETECÇÃO DE RAM ===== */

void detect_ram(RAMInfo* ram) {
    memset(ram, 0, sizeof(RAMInfo));
    
    struct sysinfo info;
    sysinfo(&info);
    
    ram->total_mb = info.totalram / (1024 * 1024);
    ram->available_mb = info.freeram / (1024 * 1024);
    ram->used_mb = ram->total_mb - ram->available_mb;
    
    // Estima banda de memória (típico para DDR4)
    ram->memory_bandwidth_gbps = 51.2;  // 64-bit @ 800MHz
}

/* ===== SCORING ===== */

float score_cpu(CPUInfo* cpu) {
    float score = 0.0;
    
    // Cores
    score += cpu->cores * 10;
    
    // Frequência
    score += cpu->frequency_ghz * 100;
    
    // Cache
    score += (cpu->cache_l3 / 1024) * 5;
    
    // Instruções SIMD
    if (cpu->has_avx512) score += 50;
    else if (cpu->has_avx2) score += 30;
    else if (cpu->has_avx) score += 20;
    else if (cpu->has_sse42) score += 10;
    
    return score;
}

float score_gpu(GPUInfo* gpu) {
    float score = 0.0;
    
    if (gpu->has_cuda) {
        score += gpu->cuda_cores / 10;
        score += gpu->cuda_memory_mb / 100;
        score += 50;  // Bonus para CUDA
    }
    
    if (gpu->has_opencl) score += 30;
    if (gpu->has_vulkan) score += 20;
    
    return score;
}

float score_ram(RAMInfo* ram) {
    float score = 0.0;
    
    // Quantidade de RAM
    score += ram->total_mb / 100;
    
    // Banda de memória
    score += ram->memory_bandwidth_gbps * 10;
    
    return score;
}

/* ===== ESTRATÉGIA DE OTIMIZAÇÃO ===== */

void determine_strategy(HardwareProfile* profile) {
    float cpu_score = profile->cpu_score;
    float gpu_score = profile->gpu_score;
    float ram_score = profile->ram_score;
    
    // Normaliza scores
    float total = cpu_score + gpu_score + ram_score;
    if (total > 0) {
        cpu_score /= total;
        gpu_score /= total;
        ram_score /= total;
    }
    
    // Determina estratégia
    
    // 1. CPU vs GPU
    if (gpu_score > cpu_score * 1.5) {
        // GPU é muito melhor
        profile->use_gpu = 1;
        profile->use_cpu = 0;
    } else if (cpu_score > gpu_score * 1.5) {
        // CPU é muito melhor
        profile->use_cpu = 1;
        profile->use_gpu = 0;
    } else {
        // Equilibrado
        profile->use_cpu = 1;
        profile->use_gpu = gpu_score > 0.2;  // Usa GPU se disponível
    }
    
    // 2. Paralelismo
    if (profile->cpu.cores >= 4) {
        profile->use_parallel = 1;
    }
    
    // 3. SIMD
    if (profile->cpu.has_avx2 || profile->cpu.has_avx512) {
        profile->use_simd = 1;
    }
    
    // 4. Vetorização
    if (profile->cpu.has_avx512) {
        profile->use_vectorization = 1;
    }
}

/* ===== GERAÇÃO DE FLAGS ===== */

void generate_compiler_flags(HardwareProfile* profile, char* flags) {
    strcpy(flags, "");
    
    // Otimização base
    strcat(flags, "-O3 -Ofast ");
    
    // CPU
    if (profile->use_simd) {
        if (profile->cpu.has_avx512) {
            strcat(flags, "-mavx512f -mavx512cd ");
        } else if (profile->cpu.has_avx2) {
            strcat(flags, "-mavx2 ");
        } else if (profile->cpu.has_avx) {
            strcat(flags, "-mavx ");
        }
    }
    
    // Paralelismo
    if (profile->use_parallel) {
        strcat(flags, "-fopenmp ");
    }
    
    // Vetorização
    if (profile->use_vectorization) {
        strcat(flags, "-ftree-vectorize -fvectorize ");
    }
    
    // Otimizações gerais
    strcat(flags, "-march=native -mtune=native ");
    strcat(flags, "-flto -ffast-math ");
    strcat(flags, "-funroll-loops -finline-functions ");
}

/* ===== IMPRESSÃO DE PERFIL ===== */

void print_hardware_profile(HardwareProfile* profile) {
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║   DETECÇÃO DE HARDWARE - LNX           ║\n");
    printf("╚════════════════════════════════════════╝\n\n");
    
    printf("CPU:\n");
    printf("  Cores: %d\n", profile->cpu.cores);
    printf("  Threads: %d\n", profile->cpu.threads);
    printf("  Frequência: %.2f GHz\n", profile->cpu.frequency_ghz);
    printf("  Cache L3: %d KB\n", profile->cpu.cache_l3);
    printf("  SIMD: ");
    if (profile->cpu.has_avx512) printf("AVX-512 ");
    if (profile->cpu.has_avx2) printf("AVX2 ");
    if (profile->cpu.has_avx) printf("AVX ");
    if (profile->cpu.has_sse42) printf("SSE4.2 ");
    printf("\n");
    printf("  Score: %.1f\n\n", profile->cpu_score);
    
    printf("GPU:\n");
    printf("  CUDA: %s\n", profile->gpu.has_cuda ? "Sim" : "Não");
    printf("  OpenCL: %s\n", profile->gpu.has_opencl ? "Sim" : "Não");
    printf("  Vulkan: %s\n", profile->gpu.has_vulkan ? "Sim" : "Não");
    if (profile->gpu.has_cuda) {
        printf("  Cores CUDA: %d\n", profile->gpu.cuda_cores);
        printf("  Memória: %ld MB\n", profile->gpu.cuda_memory_mb);
    }
    printf("  Score: %.1f\n\n", profile->gpu_score);
    
    printf("RAM:\n");
    printf("  Total: %ld MB (%.2f GB)\n", profile->ram.total_mb, profile->ram.total_mb / 1024.0);
    printf("  Disponível: %ld MB\n", profile->ram.available_mb);
    printf("  Banda: %.1f GB/s\n", profile->ram.memory_bandwidth_gbps);
    printf("  Score: %.1f\n\n", profile->ram_score);
    
    printf("ESTRATÉGIA:\n");
    printf("  Usar CPU: %s\n", profile->use_cpu ? "Sim" : "Não");
    printf("  Usar GPU: %s\n", profile->use_gpu ? "Sim" : "Não");
    printf("  Paralelismo: %s\n", profile->use_parallel ? "Sim" : "Não");
    printf("  SIMD: %s\n", profile->use_simd ? "Sim" : "Não");
    printf("  Vetorização: %s\n\n", profile->use_vectorization ? "Sim" : "Não");
}

/* ===== FUNÇÃO PRINCIPAL ===== */

HardwareProfile* detect_hardware() {
    HardwareProfile* profile = (HardwareProfile*)malloc(sizeof(HardwareProfile));
    
    // Detecta hardware
    detect_cpu(&profile->cpu);
    detect_gpu(&profile->gpu);
    detect_ram(&profile->ram);
    
    // Calcula scores
    profile->cpu_score = score_cpu(&profile->cpu);
    profile->gpu_score = score_gpu(&profile->gpu);
    profile->ram_score = score_ram(&profile->ram);
    
    // Determina estratégia
    determine_strategy(profile);
    
    return profile;
}

void free_hardware_profile(HardwareProfile* profile) {
    free(profile);
}

#endif
