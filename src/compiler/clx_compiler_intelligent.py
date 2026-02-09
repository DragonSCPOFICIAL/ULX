#!/usr/bin/env python3
"""
CLX Compiler - Inteligente e Adaptativo

Usa detecção de hardware do LNX para otimizar automaticamente
"""

import sys
import re
import subprocess
import os

class HardwareDetector:
    """Detecta hardware e determina estratégia de otimização"""
    
    def __init__(self):
        self.cpu_cores = os.cpu_count() or 1
        self.has_avx2 = self._check_avx2()
        self.has_gpu = self._check_gpu()
        self.ram_gb = self._get_ram_gb()
    
    def _check_avx2(self):
        """Verifica se CPU suporta AVX2"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                content = f.read()
                return 'avx2' in content
        except:
            return False
    
    def _check_gpu(self):
        """Verifica se GPU está disponível"""
        try:
            result = subprocess.run(['which', 'nvidia-smi'], 
                                  capture_output=True, timeout=1)
            return result.returncode == 0
        except:
            return False
    
    def _get_ram_gb(self):
        """Obtém quantidade de RAM em GB"""
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        kb = int(line.split()[1])
                        return kb / (1024 * 1024)
        except:
            return 8  # Default
    
    def get_strategy(self):
        """Retorna estratégia de otimização baseada no hardware"""
        strategy = {
            'use_parallel': self.cpu_cores >= 4,
            'use_simd': self.has_avx2,
            'use_gpu': self.has_gpu,
            'cpu_cores': self.cpu_cores,
            'ram_gb': self.ram_gb,
        }
        return strategy

class IntelligentOptimizer:
    """Otimizador inteligente que se adapta ao hardware"""
    
    def __init__(self, strategy):
        self.strategy = strategy
    
    def get_compiler_flags(self):
        """Gera flags de compilação baseadas no hardware"""
        flags = [
            'gcc',
            '-O3',
            '-Ofast',
        ]
        
        # Flags nativas apenas se suportadas
        flags.extend(['-march=native', '-mtune=native'])
        
        # Paralelismo (com verificação simples)
        if self.strategy['use_parallel']:
            # Verifica se libgomp existe para evitar erro de linkagem
            if os.path.exists('/usr/lib/libgomp.so') or os.path.exists('/usr/lib64/libgomp.so') or os.path.exists('/lib/x86_64-linux-gnu/libgomp.so.1'):
                flags.extend(['-fopenmp', '-pthread'])
        
        # SIMD
        if self.strategy['use_simd']:
            flags.extend(['-mavx2', '-ftree-vectorize'])
        
        # Otimizações gerais
        flags.extend([
            '-flto',
            '-ffast-math',
            '-funroll-loops',
            '-finline-functions',
            '-finline-limit=1000',
        ])
        
        # GPU (se disponível)
        if self.strategy['use_gpu']:
            flags.append('-DUSE_GPU')
        
        return flags
    
    def get_pragma_directives(self):
        """Retorna pragmas para inserir no código C"""
        pragmas = [
            '#pragma GCC optimize("O3")',
            '#pragma GCC optimize("Ofast")',
        ]
        
        # OpenMP pragmas removed from global scope to avoid compilation errors
        # They should be used inside functions if needed
        pass
        
        return pragmas
    
    def get_loop_optimization(self):
        """Retorna otimizações para loops"""
        if self.strategy['use_parallel'] and self.strategy['cpu_cores'] >= 8:
            return '#pragma omp parallel for simd collapse(2)'
        elif self.strategy['use_parallel']:
            return '#pragma omp parallel for'
        elif self.strategy['use_simd']:
            return '#pragma omp simd'
        else:
            return ''

class CLXCompilerIntelligent:
    """Compilador inteligente que se adapta ao hardware"""
    
    def __init__(self, source_file):
        self.source_file = source_file
        self.source = None
        self.detector = HardwareDetector()
        self.strategy = self.detector.get_strategy()
        self.optimizer = IntelligentOptimizer(self.strategy)
    
    def read_source(self):
        """Lê arquivo ULX"""
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                self.source = f.read()
            return True
        except FileNotFoundError:
            print(f"[CLX] ✗ Erro: Arquivo '{self.source_file}' não encontrado")
            return False
    
    def print_hardware_info(self):
        """Imprime informações de hardware detectado"""
        print("\n[CLX] ╔════════════════════════════════════════╗")
        print("[CLX] ║   DETECÇÃO DE HARDWARE - LNX           ║")
        print("[CLX] ╚════════════════════════════════════════╝")
        print(f"\n[CLX] CPU: {self.strategy['cpu_cores']} cores")
        print(f"[CLX] RAM: {self.strategy['ram_gb']:.1f} GB")
        print(f"[CLX] AVX2: {'Sim' if self.strategy['use_simd'] else 'Não'}")
        print(f"[CLX] GPU: {'Sim' if self.strategy['use_gpu'] else 'Não'}")
        print(f"\n[CLX] ESTRATÉGIA:")
        print(f"[CLX]   Paralelismo: {'Sim' if self.strategy['use_parallel'] else 'Não'}")
        print(f"[CLX]   SIMD: {'Sim' if self.strategy['use_simd'] else 'Não'}")
        print(f"[CLX]   GPU: {'Sim' if self.strategy['use_gpu'] else 'Não'}")
    
    def tokenize(self):
        """Tokeniza código ULX"""
        lines = self.source.split('\n')
        processed = []
        
        for line in lines:
            if '//' in line:
                line = line[:line.index('//')]
            
            line = line.strip()
            if line:
                processed.append(line)
        
        return processed
    
    def parse_line(self, line):
        """Converte linha ULX em C"""
        
        if line.startswith('escreva('):
            # Caso com múltiplos argumentos
            content = line[line.find('(')+1:line.rfind(')')]
            # Regex melhorada para capturar strings e variáveis corretamente
            parts = re.findall(r'"[^"]*"|[\w\.]+', content)
            c_parts = []
            for p in parts:
                if p.startswith('"'):
                    c_parts.append(f'printf("%s", {p});')
                else:
                    # Heuristica de tipo: se termina com _nivel, _temp, _uso, ou e 'i', 'j', 'x', e inteiro
                    if any(x in p for x in ['nivel', 'temp', 'uso', 'cores', 'total', 'usada', 'livre']):
                        c_parts.append(f'printf("%d", {p});')
                    elif any(x in p for x in ['modelo', 'nome', 'status', 'sistema', 'uptime']):
                        c_parts.append(f'printf("%s", {p});')
                    else:
                        c_parts.append(f'printf("%d", {p});')
            return " ".join(c_parts)
        
        if '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
            parts = line.split('=', 1)
            var = parts[0].strip()
            value = parts[1].strip()
            if value.startswith('"'):
                return f'const char* {var} = {value};'
            # Suporte para expressões matemáticas simples na atribuição
            return f'int {var} = {value};'
        
        if line.startswith('para ('):
            match = re.search(r'para\s*\(\s*(.+?)\s*;\s*(.+?)\s*;\s*(.+?)\s*\)\s*\{?', line)
            if match:
                init, cond, inc = match.groups()
                loop_opt = self.optimizer.get_loop_optimization()
                if loop_opt:
                    return f'{loop_opt}\nfor ({init}; {cond}; {inc}) {{'
                else:
                    return f'for ({init}; {cond}; {inc}) {{'

        if line.startswith('se ('):
            match = re.search(r'se\s*\((.+)\)\s*\{?', line)
            if match:
                return f'if ({match.group(1)}) {{'

        if line.startswith('senao'):
            if '{' in line:
                return '} else {'
            return '} else'

        if line == '}':
            return '}'
        
        return None
    
    def generate_c_code(self, tokens):
        """Gera código C otimizado para o hardware"""
        c_code = []
        
        # Headers
        c_code.append('#include <stdio.h>')
        c_code.append('#include <stdlib.h>')
        c_code.append('#include <string.h>')
        c_code.append('')
        
        # Pragmas de otimização
        for pragma in self.optimizer.get_pragma_directives():
            c_code.append(pragma)
        c_code.append('')
        
        c_code.append('int main() {')
        
        indent_level = 1
        
        for line in tokens:
            c_line = self.parse_line(line)
            
            if c_line:
                if c_line.startswith('}'):
                    indent_level = max(0, indent_level - 1)
                
                indent = '    ' * indent_level
                c_code.append(indent + c_line)
                
                if c_line.endswith('{'):
                    indent_level += 1
        
        c_code.append('    return 0;')
        c_code.append('}')
        
        return '\n'.join(c_code)
    
    def compile(self):
        """Compila ULX com otimizações inteligentes"""
        
        if not self.read_source():
            return False
        
        print("\n[CLX] ╔════════════════════════════════════════╗")
        print("[CLX] ║   COMPILADOR INTELIGENTE CLX           ║")
        print("[CLX] ║   Adaptativo ao Hardware               ║")
        print("[CLX] ╚════════════════════════════════════════╝")
        
        self.print_hardware_info()
        
        print("\n[CLX] Fase 1: Análise Léxica")
        tokens = self.tokenize()
        print(f"[CLX] ✓ {len(tokens)} linhas processadas")
        
        print("\n[CLX] Fase 2: Geração de Código C")
        c_code = self.generate_c_code(tokens)
        
        c_file = self.source_file.replace('.ulx', '.c')
        with open(c_file, 'w') as f:
            f.write(c_code)
        print(f"[CLX] ✓ Código C otimizado: {c_file}")
        
        print("\n[CLX] Fase 3: Compilação com Otimizações Inteligentes")
        
        binary_file = self.source_file.replace('.ulx', '')
        
        compile_flags = self.optimizer.get_compiler_flags()
        compile_flags.extend(['-static', '-s', c_file, '-o', binary_file, '-lm'])
        
        try:
            result = subprocess.run(
                compile_flags,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                size = os.path.getsize(binary_file)
                print(f"[CLX] ✓ Binário gerado: {binary_file}")
                print(f"[CLX] ✓ Tamanho: {size} bytes")
                print(f"\n[CLX] ╔════════════════════════════════════════╗")
                print("[CLX] ║   COMPILAÇÃO BEM-SUCEDIDA              ║")
                print("[CLX] ║   Otimizado para seu hardware          ║")
                print("[CLX] ╚════════════════════════════════════════╝")
                print(f"\n[CLX] Execute com: ./{binary_file}\n")
                return True
            else:
                print(f"[CLX] ✗ Erro na compilação:")
                print(result.stderr)
                return False
        
        except FileNotFoundError:
            print("[CLX] ✗ Erro: gcc não encontrado")
            return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 clx_compiler_intelligent.py <arquivo.ulx>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    compiler = CLXCompilerIntelligent(source_file)
    success = compiler.compile()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
