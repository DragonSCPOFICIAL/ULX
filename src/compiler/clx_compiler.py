#!/usr/bin/env python3
"""
CLX Compiler - O Compilador Mágico que Transforma ULX em Binário

ULX é fácil. CLX faz toda a complexidade invisível.
"""

import sys
import re

class CLXCompiler:
    """O Compilador Principal - Faz toda a Mágica"""
    
    def __init__(self, source_file):
        self.source_file = source_file
        self.source = None
        self.variables = set()
    
    def read_source(self):
        """Lê arquivo ULX"""
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                self.source = f.read()
            print(f"[CLX] ✓ Arquivo lido: {self.source_file}")
            return True
        except FileNotFoundError:
            print(f"[CLX] ✗ Erro: Arquivo '{self.source_file}' não encontrado")
            return False
    
    def tokenize(self):
        """Converte código ULX em linhas processáveis"""
        lines = self.source.split('\n')
        processed = []
        
        for line in lines:
            # Remove comentários
            if '//' in line:
                line = line[:line.index('//')]
            
            line = line.strip()
            if line:
                processed.append(line)
        
        return processed
    
    def parse_escreva(self, line):
        """Processa escreva()"""
        # escreva("texto")
        match = re.search(r'escreva\s*\(\s*"([^"]*)"\s*\)', line)
        if match:
            text = match.group(1)
            return f'printf("{text}\\n");'
        
        # escreva(variável)
        match = re.search(r'escreva\s*\(\s*([a-zA-Z_]\w*)\s*\)', line)
        if match:
            var = match.group(1)
            return f'printf("%d\\n", {var});'
        
        # escreva(expressão com strings)
        match = re.search(r'escreva\s*\(\s*"([^"]*)"\s*\+\s*(.+)\s*\)', line)
        if match:
            text = match.group(1)
            expr = match.group(2)
            return f'printf("{text}%d\\n", {expr});'
        
        # escreva(expressão)
        match = re.search(r'escreva\s*\(\s*(.+)\s*\)', line)
        if match:
            expr = match.group(1)
            return f'printf("%d\\n", {expr});'
        
        return None
    
    def parse_line(self, line):
        """Converte uma linha ULX em C"""
        
        # escreva(...)
        if line.startswith('escreva('):
            return self.parse_escreva(line)
        
        # Atribuição: a = 10 ou a = b + c
        if '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
            parts = line.split('=', 1)
            var = parts[0].strip()
            value = parts[1].strip()
            
            # Registra variável
            if var not in self.variables:
                self.variables.add(var)
                return f'int {var} = {value};'
            else:
                return f'{var} = {value};'
        
        # para (i = 1; i <= 10; i = i + 1) {
        if line.startswith('para ('):
            match = re.search(r'para\s*\(\s*(.+?)\s*;\s*(.+?)\s*;\s*(.+?)\s*\)\s*\{?', line)
            if match:
                init = match.group(1)
                cond = match.group(2)
                inc = match.group(3)
                
                # Extrai variável do init para declarar
                var_match = re.search(r'(\w+)\s*=', init)
                if var_match:
                    var = var_match.group(1)
                    if var not in self.variables:
                        self.variables.add(var)
                        # Declara a variável e cria o for
                        return f'int {init}; for ({var} = {init.split("=")[1].strip()}; {cond}; {inc}) {{'
                
                return f'for ({init}; {cond}; {inc}) {{'
        
        # enquanto (condição) {
        if line.startswith('enquanto ('):
            match = re.search(r'enquanto\s*\(\s*(.+?)\s*\)\s*\{?', line)
            if match:
                cond = match.group(1)
                return f'while ({cond}) {{'
        
        # se (condição) {
        if line.startswith('se ('):
            match = re.search(r'se\s*\(\s*(.+?)\s*\)\s*\{?', line)
            if match:
                cond = match.group(1)
                return f'if ({cond}) {{'
        
        # senao {
        if line.startswith('senao'):
            return '} else {'
        
        # Chaves
        if line == '{':
            return None  # Ignorar chaves soltas
        if line == '}':
            return '}'
        
        return None
    
    def generate_c_code(self, tokens):
        """Gera código C a partir dos tokens ULX"""
        c_code = []
        
        c_code.append('#include <stdio.h>')
        c_code.append('#include <stdlib.h>')
        c_code.append('#include <string.h>')
        c_code.append('')
        c_code.append('int main() {')
        
        indent_level = 1
        
        for line in tokens:
            c_line = self.parse_line(line)
            
            if c_line:
                # Reduz indentação para }
                if c_line.startswith('}'):
                    indent_level = max(0, indent_level - 1)
                
                indent = '    ' * indent_level
                c_code.append(indent + c_line)
                
                # Aumenta indentação para {
                if c_line.endswith('{'):
                    indent_level += 1
        
        c_code.append('    return 0;')
        c_code.append('}')
        
        return '\n'.join(c_code)
    
    def compile(self):
        """Compila ULX → C → Binário"""
        
        if not self.read_source():
            return False
        
        print("[CLX] Iniciando compilação...")
        print("[CLX] Fase 1: Análise Léxica (Tokenização)")
        
        # Fase 1: Tokenize
        tokens = self.tokenize()
        print(f"[CLX] ✓ {len(tokens)} linhas processadas")
        
        print("[CLX] Fase 2: Geração de Código (C Intermediário)")
        
        # Fase 2: Generate C code
        c_code = self.generate_c_code(tokens)
        
        # Salva código C intermediário
        c_file = self.source_file.replace('.ulx', '.c')
        with open(c_file, 'w') as f:
            f.write(c_code)
        print(f"[CLX] ✓ Código C intermediário: {c_file}")
        
        print("[CLX] Fase 3: Compilação C → Binário (LNX Integration)")
        
        # Fase 3: Compila C para binário
        binary_file = self.source_file.replace('.ulx', '')
        import subprocess
        
        try:
            result = subprocess.run(
                ['gcc', '-O3', '-static', c_file, '-o', binary_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"[CLX] ✓ Binário gerado: {binary_file}")
                print(f"[CLX] ✓ Compilação bem-sucedida!")
                print(f"[CLX] Execute com: ./{binary_file}")
                return True
            else:
                print(f"[CLX] ✗ Erro na compilação C:")
                print(result.stderr)
                return False
        
        except FileNotFoundError:
            print("[CLX] ✗ Erro: gcc não encontrado. Instale com: sudo apt install build-essential")
            return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 clx_compiler.py <arquivo.ulx>")
        print("\nExemplo:")
        print("  python3 clx_compiler.py hello_world.ulx")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    print("=" * 60)
    print("CLX COMPILER - O Compilador Mágico do ULX")
    print("=" * 60)
    
    compiler = CLXCompiler(source_file)
    success = compiler.compile()
    
    print("=" * 60)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
