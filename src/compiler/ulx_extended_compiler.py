#!/usr/bin/env python3
"""
ULX Extended Compiler - Exemplo de como estender ULX

Este compilador mostra como criar uma linguagem baseada em ULX
com recursos adicionais, mantendo toda a performance.
"""

import sys
import re
import subprocess

# Importa o compilador base
from clx_compiler import CLXCompiler, CLXOptimizer

class ULXExtendedCompiler(CLXCompiler):
    """Estende CLX com recursos adicionais"""
    
    def __init__(self, source_file):
        super().__init__(source_file)
        self.functions = {}
        self.arrays = {}
    
    def parse_array_declaration(self, line):
        """Processa declaração de arrays: lista[10] = [1,2,3...]"""
        match = re.search(r'lista\s+(\w+)\[(\d+)\]\s*=\s*\[([^\]]+)\]', line)
        if match:
            name, size, values = match.groups()
            self.arrays[name] = (size, values)
            
            # Gera código C para array
            values_list = ', '.join(values.split(','))
            return f'int {name}[] = {{{values_list}}};'
        
        return None
    
    def parse_function_def(self, line):
        """Processa definição de função: func nome(param1, param2) { ... }"""
        match = re.search(r'func\s+(\w+)\s*\((.*?)\)\s*\{?', line)
        if match:
            name, params = match.groups()
            self.functions[name] = params
            
            # Gera código C para função
            return f'int {name}({params}) {{'
        
        return None
    
    def parse_return_statement(self, line):
        """Processa retorno: volta valor"""
        match = re.search(r'volta\s+(.+)', line)
        if match:
            value = match.group(1)
            return f'return {value};'
        
        return None
    
    def parse_for_each(self, line):
        """Processa for-each: para_cada item em lista { ... }"""
        match = re.search(r'para_cada\s+(\w+)\s+em\s+(\w+)\s*\{?', line)
        if match:
            item, array = match.groups()
            
            # Gera loop for-each
            if array in self.arrays:
                size = self.arrays[array][0]
                return f'for (int i = 0; i < {size}; i++) {{ int {item} = {array}[i];'
        
        return None
    
    def parse_extended_line(self, line):
        """Processa sintaxe estendida antes de chamar parser base"""
        
        # Tenta sintaxe estendida
        result = self.parse_array_declaration(line)
        if result:
            return result
        
        result = self.parse_function_def(line)
        if result:
            return result
        
        result = self.parse_return_statement(line)
        if result:
            return result
        
        result = self.parse_for_each(line)
        if result:
            return result
        
        # Se não é sintaxe estendida, tenta sintaxe base ULX
        return self.parse_line(line)
    
    def generate_c_code(self, tokens):
        """Gera código C com suporte a sintaxe estendida"""
        c_code = []
        
        # Headers
        c_code.append('#include <stdio.h>')
        c_code.append('#include <stdlib.h>')
        c_code.append('#include <string.h>')
        c_code.append('#include <stdint.h>')
        c_code.append('')
        
        # Pragmas de otimização
        c_code.append('#pragma GCC optimize("O3")')
        c_code.append('#pragma GCC optimize("inline")')
        c_code.append('#pragma GCC optimize("unroll-loops")')
        c_code.append('#pragma GCC target("avx2")')
        c_code.append('')
        
        c_code.append('int main() {')
        
        indent_level = 1
        
        for line in tokens:
            c_line = self.parse_extended_line(line)
            
            if c_line:
                if c_line.startswith('}'):
                    indent_level = max(0, indent_level - 1)
                
                indent = '    ' * indent_level
                c_code.append(indent + c_line)
                
                if c_line.endswith('{'):
                    indent_level += 1
        
        c_code.append('    return 0;')
        c_code.append('}')
        
        c_code_str = '\n'.join(c_code)
        
        # Aplica otimizações
        c_code_str = self.optimizer.inline_constants(c_code_str)
        c_code_str = self.optimizer.eliminate_dead_code(c_code_str)
        c_code_str = self.optimizer.loop_unrolling(c_code_str)
        
        return c_code_str
    
    def compile(self):
        """Compila com suporte a sintaxe estendida"""
        
        if not self.read_source():
            return False
        
        print("[ULX-EXTENDED] ╔════════════════════════════════════════╗")
        print("[ULX-EXTENDED] ║   COMPILADOR ESTENDIDO DE ULX          ║")
        print("[ULX-EXTENDED] ║   Com recursos avançados               ║")
        print("[ULX-EXTENDED] ╚════════════════════════════════════════╝")
        print()
        
        print("[ULX-EXTENDED] Fase 1: Análise Léxica")
        tokens = self.tokenize()
        print(f"[ULX-EXTENDED] ✓ {len(tokens)} linhas processadas")
        print()
        
        print("[ULX-EXTENDED] Fase 2: Geração de Código C Otimizado")
        c_code = self.generate_c_code(tokens)
        
        c_file = self.source_file.replace('.ulx', '.c')
        with open(c_file, 'w') as f:
            f.write(c_code)
        print(f"[ULX-EXTENDED] ✓ Código C otimizado: {c_file}")
        print()
        
        print("[ULX-EXTENDED] Fase 3: Compilação com Otimizações Agressivas")
        
        binary_file = self.source_file.replace('.ulx', '')
        
        compile_flags = [
            'gcc',
            '-O3',
            '-march=native',
            '-flto',
            '-ffast-math',
            '-funroll-loops',
            '-finline-functions',
            '-static',
            '-s',
            c_file,
            '-o', binary_file
        ]
        
        try:
            result = subprocess.run(
                compile_flags,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                import os
                size = os.path.getsize(binary_file)
                print(f"[ULX-EXTENDED] ✓ Binário gerado: {binary_file}")
                print(f"[ULX-EXTENDED] ✓ Tamanho: {size} bytes")
                print(f"[ULX-EXTENDED] ✓ Compilação bem-sucedida!")
                print()
                print("[ULX-EXTENDED] ╔════════════════════════════════════════╗")
                print("[ULX-EXTENDED] ║   EXTENSÃO COMPILADA COM SUCESSO       ║")
                print("[ULX-EXTENDED] ║   Herdando performance extrema de ULX   ║")
                print("[ULX-EXTENDED] ╚════════════════════════════════════════╝")
                return True
            else:
                print(f"[ULX-EXTENDED] ✗ Erro na compilação:")
                print(result.stderr)
                return False
        
        except FileNotFoundError:
            print("[ULX-EXTENDED] ✗ Erro: gcc não encontrado")
            return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 ulx_extended_compiler.py <arquivo.ulx>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    compiler = ULXExtendedCompiler(source_file)
    success = compiler.compile()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
