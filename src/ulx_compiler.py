import sys
import os

def transpile_to_c(dragon_code):
    c_code = """
#include <stdio.h>
#include <stdlib.h>

int main() {
"""
    
    for line in dragon_code.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith("print(") and stripped_line.endswith(")"):
            message = stripped_line[len("print("): -1].strip()
            c_code += f"    printf(%s\n, {message});\n"
        elif stripped_line.startswith("func main() {"):
            # Ignore main function definition in DL, C has its own
            pass
        elif stripped_line.startswith("}"):
            # Ignore closing brace for now, will be added at the end
            pass
        elif stripped_line.startswith("//") or not stripped_line:
            # Ignore comments and empty lines
            pass
        else:
            # For now, just pass through unrecognized lines as comments
            c_code += f"    // {stripped_line} (unrecognized Dragon-Lang syntax)\n"

    c_code += """
    return 0;
}
"""
    return c_code

def main():
    if len(sys.argv) < 2:
        print("Uso: dragon <arquivo.dl>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith(".dl"):
        print("Erro: O arquivo de entrada deve ter a extensão .dl")
        sys.exit(1)

    output_c_file = input_file.replace(".dl", ".c")
    output_bin_file = input_file.replace(".dl", "")

    try:
        with open(input_file, "r") as f:
            dragon_code = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
        sys.exit(1)

    c_code = transpile_to_c(dragon_code)

    with open(output_c_file, "w") as f:
        f.write(c_code)
    
    print(f"Transpilado '{input_file}' para '{output_c_file}'")

    # Compilar o código C para um binário estático
    compile_command = f"gcc -static {output_c_file} -o {output_bin_file}"
    print(f"Compilando para binário estático: {compile_command}")
    os.system(compile_command)

    if os.path.exists(output_bin_file):
        print(f"Binário estático '{output_bin_file}' criado com sucesso.")
        os.chmod(output_bin_file, 0o755) # Make it executable
    else:
        print("Erro na compilação do binário estático.")

if __name__ == "__main__":
    main()
