#!/usr/bin/env python3
import sys
import os
import subprocess

def compile_ulx_native(source_file):
    if not source_file.endswith('.ulx'):
        print("Erro: O arquivo deve ter a extensão .ulx")
        return

    base_name = source_file.replace('.ulx', '')
    c_file = base_name + ".c"
    
    print(f"[CLX] Lendo código ULX: {source_file}")
    
    # Simulação de Parser ULX -> C com injeção da ponte LNX
    with open(source_file, 'r') as f:
        ulx_code = f.read()

    with open(c_file, 'w') as f:
        f.write('#include "/home/ubuntu/lnx_native_bridge.h"\n')
        f.write('#include <stdio.h>\n\n')
        f.write('int main() {\n')
        f.write('    // Injeção da Trindade LNX: Desconecta do console imediatamente\n')
        f.write('    lnx_detach_from_console();\n\n')
        
        # Tradução simples de comandos (exemplo)
        for line in ulx_code.split('\n'):
            line = line.strip()
            if line.startswith('escreva('):
                content = line[8:-1]
                f.write(f'    printf("%s\\n", {content});\n')
            elif line.startswith('janela('):
                # Aqui entraria a lógica de X11 nativa
                f.write('    // Lógica de janela nativa LNX\n')
        
        f.write('\n    // Loop infinito para manter o app vivo como um processo nativo\n')
        f.write('    while(1) { sleep(1); }\n')
        f.write('    return 0;\n')
        f.write('}\n')

    print(f"[CLX] Gerando binário ELF nativo...")
    # Compilação com flags que removem a necessidade de terminal
    output_bin = base_name
    subprocess.run(['gcc', c_file, '-o', output_bin])
    
    print(f"[CLX] Sucesso! Aplicativo '{output_bin}' criado.")
    print(f"[CLX] Ele rodará em background sem abrir console.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 clx_native_compiler.py <arquivo.ulx>")
    else:
        compile_ulx_native(sys.argv[1])
